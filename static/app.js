// static/app.js

class ASCIIWebcam {
    constructor() {
        this.display = document.getElementById('ascii-display');
        this.status = document.getElementById('status');
        this.video = document.getElementById('webcam-feed');
        this.canvas = document.getElementById('capture-canvas');
        this.context = this.canvas.getContext('2d', { willReadFrequently: true });

        this.socket = null;
        this.stream = null;
        this.captureInterval = null;
        this.FRAME_RATE = 15; // Capture and send 15 frames per second
        
        this.init();
    }
 
    async init() {
        try {
            // Request webcam access from the user
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 640, height: 480 },
                audio: false 
            });
            this.video.srcObject = this.stream;
            this.video.style.display = 'block'; // Show the video feed
            this.status.textContent = "Camera accessed. Connecting to server...";
            this.connect();
        } catch (err) {
            this.status.textContent = 'Error: Could not access webcam. Please grant permission.';
            this.status.className = 'status disconnected';
            this.display.textContent = `Error: ${err.name}\n\nThis feature requires camera permissions. Please allow access and refresh the page.`;
        }
    }
    
    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        // Connect to the single '/ws' endpoint
        const wsUrl = `${protocol}//${window.location.host}/ws`; 
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => {
            this.status.textContent = 'Connected! Streaming video...';
            this.status.className = 'status connected';
            this.startFrameCapture();
        };
        
        this.socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'frame') {
                this.display.innerHTML = this.ansiToHtml(message.data);
            }
        };
        
        this.socket.onclose = () => {
            this.status.textContent = 'Disconnected.';
            this.status.className = 'status disconnected';
            this.stopFrameCapture();
        };
        
        this.socket.onerror = (error) => {
            this.status.textContent = 'Connection Error.';
            this.status.className = 'status disconnected';
        };
    }

    startFrameCapture() {
        if (this.captureInterval) return;
        this.captureInterval = setInterval(() => {
            if (this.socket.readyState !== WebSocket.OPEN) return;
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
            this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            const frameData = this.canvas.toDataURL('image/jpeg', 0.6); // Use JPEG with 60% quality
            this.socket.send(frameData);
        }, 1000 / this.FRAME_RATE);
    }
    
    stopFrameCapture() {
        clearInterval(this.captureInterval);
        this.captureInterval = null;
    }

    ansiToHtml(ansiData) {
        return ansiData
            .replace(/\033\[38;2;(\d+);(\d+);(\d+)m/g, '<span style="color: rgb($1, $2, $3);">')
            .replace(/\033\[0m/g, '</span>');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ASCIIWebcam();
});