class ASCIIWebcam {
    constructor() {
        this.socket = null;
        this.display = document.getElementById('ascii-display');
        this.status = document.getElementById('status');
        this.toggleBtn = document.getElementById('toggleBtn');
        this.isRunning = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        
        this.init();
    }
    
    init() {
        this.connect();
        this.toggleBtn.addEventListener('click', () => this.toggle());
    }
    
    connect() {
        // Use correct WebSocket URL for Render
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.status.textContent = 'Connecting...';
        this.status.className = 'status';
        
        try {
            this.socket = new WebSocket(wsUrl);
            
            this.socket.onopen = () => {
                console.log('WebSocket connected');
                this.status.textContent = 'Connected - Streaming ASCII Art';
                this.status.className = 'status connected';
                this.isRunning = true;
                this.reconnectAttempts = 0;
            };
            
            this.socket.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    if (message.type === 'frame') {
                        this.displayFrame(message.data);
                    }
                } catch (error) {
                    console.error('Error parsing message:', error);
                }
            };
            
            this.socket.onclose = (event) => {
                console.log('WebSocket closed:', event.code, event.reason);
                this.status.textContent = 'Disconnected';
                this.status.className = 'status disconnected';
                this.isRunning = false;
                
                // Exponential backoff reconnection
                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
                    this.reconnectAttempts++;
                    setTimeout(() => this.connect(), delay);
                }
            };
            
            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.status.textContent = 'Connection Error - Retrying...';
                this.status.className = 'status disconnected';
            };
            
        } catch (error) {
            console.error('Failed to create WebSocket:', error);
            this.status.textContent = 'Failed to create connection';
            this.status.className = 'status disconnected';
        }
    }
    
    displayFrame(asciiData) {
        // Convert ANSI codes to HTML with better error handling
        try {
            let htmlData = asciiData
                .replace(/\033\[38;2;(\d+);(\d+);(\d+)m/g, '<span style="color: rgb($1, $2, $3);">')
                .replace(/\033\[0m/g, '</span>');
            
            this.display.innerHTML = htmlData;
        } catch (error) {
            console.error('Error displaying frame:', error);
        }
    }
    
    toggle() {
        if (this.isRunning && this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.close();
        } else {
            this.reconnectAttempts = 0;
            this.connect();
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new ASCIIWebcam();
});