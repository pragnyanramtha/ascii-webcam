class ASCIIWebcam {
    constructor() {
        this.socket = null;
        this.display = document.getElementById('ascii-display');
        this.status = document.getElementById('status');
        this.toggleBtn = document.getElementById('toggleBtn');
        this.isRunning = false;
        
        this.init();
    }
    
    init() {
        this.connect();
        this.toggleBtn.addEventListener('click', () => this.toggle());
    }
    
    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => {
            this.status.textContent = 'Connected';
            this.status.className = 'status connected';
            this.isRunning = true;
        };
        
        this.socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'frame') {
                this.displayFrame(message.data);
            }
        };
        
        this.socket.onclose = () => {
            this.status.textContent = 'Disconnected';
            this.status.className = 'status disconnected';
            this.isRunning = false;
            
            // Reconnect after 3 seconds
            setTimeout(() => this.connect(), 3000);
        };
        
        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.status.textContent = 'Connection Error';
            this.status.className = 'status disconnected';
        };
    }
    
    displayFrame(asciiData) {
        // Convert ANSI codes to HTML
        let htmlData = asciiData
            .replace(/\033\[38;2;(\d+);(\d+);(\d+)m/g, '<span style="color: rgb($1, $2, $3);">')
            .replace(/\033\[0m/g, '</span>');
        
        this.display.innerHTML = htmlData;
    }
    
    toggle() {
        if (this.isRunning) {
            this.socket.close();
        } else {
            this.connect();
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new ASCIIWebcam();
});