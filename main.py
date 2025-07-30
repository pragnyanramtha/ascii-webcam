# main.py
import base64
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# --- Constants and Configuration ---
ASCII_CHARS = " .:-=+*#%@"
ASCII_WIDTH = 120  # The width of the resulting ASCII art
ASCII_HEIGHT = 45 # The height of the resulting ASCII art

# --- FastAPI App Setup ---
app = FastAPI()

# Mount the 'static' directory to serve HTML, CSS, and JS
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Image and ASCII Processing Functions ---

def apply_clahe(img):
    """Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) for better contrast."""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

def frame_to_colored_ascii(frame):
    """Converts an OpenCV frame to a colored ASCII string using ANSI escape codes."""
    # 1. Resize the frame to the desired ASCII dimensions
    resized_frame = cv2.resize(frame, (ASCII_WIDTH, ASCII_HEIGHT))
    
    # 2. Apply contrast enhancement to prevent dark spots
    enhanced_frame = apply_clahe(resized_frame)
    
    # 3. Create a grayscale version to map pixel brightness to characters
    gray_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2GRAY)
    
    # 4. Build the ASCII string with embedded color codes
    ascii_rows = []
    for i in range(ASCII_HEIGHT):
        row_str = ""
        for j in range(ASCII_WIDTH):
            # Get character based on brightness
            brightness = gray_frame[i, j]
            char_index = int((brightness / 255) * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[char_index]
            
            # Get the original color from the enhanced (and resized) frame
            b, g, r = enhanced_frame[i, j]
            
            # Embed ANSI color code directly into the string
            row_str += f"\033[38;2;{r};{g};{b}m{char}"
        
        ascii_rows.append(row_str)
        
    # Return the full string with a final reset code
    return "\n".join(ascii_rows) + "\033[0m"


# --- FastAPI Routes ---

@app.get("/")
async def get_index():
    """Serves the main index.html file."""
    return FileResponse('static/index.html')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles the WebSocket connection for receiving webcam frames and sending back ASCII art."""
    await websocket.accept()
    print("Client connected.")
    try:
        while True:
            # Receive base64 encoded image string from the client
            data = await websocket.receive_text()
            
            # Decode the base64 string to image bytes
            header, encoded = data.split(",", 1)
            img_data = base64.b64decode(encoded)
            
            # Convert image bytes to a NumPy array
            nparr = np.frombuffer(img_data, np.uint8)
            
            # Decode the NumPy array into an OpenCV image (frame)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Process the frame to get the colored ASCII string
            ascii_string = frame_to_colored_ascii(frame)
            
            # Send the result back to the client
            await websocket.send_json({"type": "frame", "data": ascii_string})

    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await websocket.close()