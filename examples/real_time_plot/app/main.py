# app/main.py
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import uvicorn
from queue_handler import data_queue
from data_producer import start_producer

from fastapi.responses import FileResponse


app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
def read_root():
    return FileResponse("static/index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = data_queue.get()
        await websocket.send_json(data)

if __name__ == "__main__":
    start_producer()
    uvicorn.run(app, host="0.0.0.0", port=8000)
