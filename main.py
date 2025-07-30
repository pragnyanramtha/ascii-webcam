import asyncio
import cv2
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from ascii_converter import ASCIIConverter
import threading
import time

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variables
converter = ASCIIConverter()
active_connections = []
camera = None
streaming = False

@app.get("/")
async def get():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Keep connection alive
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

def camera_stream():
    """Camera streaming thread"""
    global camera, streaming
    
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FPS, 20)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    streaming = True
    
    while streaming:
        ret, frame = camera.read()
        if not ret:
            continue
            
        # Convert to ASCII
        ascii_frame = converter.frame_to_ascii(frame)
        
        # Send to all connected clients
        message = json.dumps({"type": "frame", "data": ascii_frame})
        
        # Remove disconnected clients
        disconnected = []
        for connection in active_connections:
            try:
                asyncio.create_task(connection.send_text(message))
            except:
                disconnected.append(connection)
        
        for conn in disconnected:
            if conn in active_connections:
                active_connections.remove(conn)
        
        time.sleep(1/20)  # 20 FPS
    
    if camera:
        camera.release()

@app.on_event("startup")
async def startup_event():
    # Start camera stream in background thread
    thread = threading.Thread(target=camera_stream, daemon=True)
    thread.start()

@app.on_event("shutdown")
async def shutdown_event():
    global streaming
    streaming = False

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)