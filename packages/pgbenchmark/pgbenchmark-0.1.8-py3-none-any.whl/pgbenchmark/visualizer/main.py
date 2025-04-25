import os
import tempfile

import psycopg2
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pgbenchmark import Benchmark

app = FastAPI()
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    paused = False
    stop_requested = False

    try:
        init = await websocket.receive_json()
    except WebSocketDisconnect:
        return

    if init.get("type") == "start":
        conn_str = init.get("connection")
        sql_text = init.get("sql")
        runs = int(init.get("runs", 1))

        conn = psycopg2.connect(conn_str)
        benchmark = Benchmark(db_connection=conn, number_of_runs=runs)

        with tempfile.NamedTemporaryFile("w+", suffix=".sql", delete=False) as f:
            f.write(sql_text)
            f.flush()
            benchmark.set_sql(f.name)

    async def consumer():
        nonlocal paused, stop_requested
        try:
            while True:
                msg = await websocket.receive_json()
                if msg.get("type") == "pause":
                    paused = True
                elif msg.get("type") == "resume":
                    paused = False
                elif msg.get("type") == "stop":
                    stop_requested = True
                    break
        except WebSocketDisconnect:
            stop_requested = True

    async def producer():
        nonlocal paused, stop_requested
        try:
            for result in benchmark:
                if stop_requested:
                    break
                while paused:
                    if stop_requested:
                        break
                    # Busy-wait pause; could add sleep
                    await websocket.receive_text()
                payload = {"timestamp": result["sent_at"], "value": float(result["duration"])}
                await websocket.send_json(payload)
        except WebSocketDisconnect:
            pass
        finally:
            conn.close()

    # Run consumer and producer concurrently
    import asyncio
    await asyncio.gather(producer(), consumer())
