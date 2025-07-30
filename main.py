import asyncio
import cv2
import json
import os
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
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)

def camera_stream():
    """Mock camera stream for cloud deployment"""
    global streaming
    streaming = True
    
    # Create a simple test pattern since webcam isn't available on cloud
    import numpy as np
    
    frame_count = 0
    while streaming:
        # Create animated test pattern
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Moving gradient
        for y in range(480):
            for x in range(640):
                r = int((x + frame_count) % 256)
                g = int((y + frame_count * 2) % 256)
                b = int((x + y + frame_count) % 256)
                frame[y, x] = [b, g, r]  # BGR format
        
        # Convert to ASCII
        ascii_frame = converter.frame_to_ascii(frame)
        
        # Send to all connected clients
        message = json.dumps({"type": "frame", "data": ascii_frame})
        
        # Send to active connections
        disconnected = []
        for connection in active_connections:
            try:
                # Use asyncio.run_coroutine_threadsafe for thread safety
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(connection.send_text(message))
                loop.close()
            except:
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            if conn in active_connections:
                active_connections.remove(conn)
        
        frame_count += 1
        time.sleep(1/15)  # 15 FPS for better performance

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
    # Use PORT environment variable for Render
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)