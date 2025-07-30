import cv2
import numpy as np

class ASCIIConverter:
    def __init__(self):
        # ASCII characters from light to dark
        self.ascii_chars = " .:-=+*#%@"
        self.width = 80
        self.height = 60
        
    def preprocess_frame(self, frame):
        """Apply CLAHE and blur to eliminate dark spots"""
        # Resize frame
        frame = cv2.resize(frame, (self.width, self.height))
        
        # Apply CLAHE to each color channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Apply slight blur to reduce noise
        frame = cv2.GaussianBlur(frame, (3,3), 0)
        
        return frame
    
    def pixel_to_ascii(self, pixel_value):
        """Convert pixel brightness to ASCII character"""
        return self.ascii_chars[min(pixel_value * len(self.ascii_chars) // 256, len(self.ascii_chars) - 1)]
    
    def rgb_to_ansi(self, r, g, b):
        """Convert RGB to ANSI color code"""
        return f"\033[38;2;{r};{g};{b}m"
    
    def frame_to_ascii(self, frame):
        """Convert entire frame to colored ASCII"""
        processed_frame = self.preprocess_frame(frame)
        ascii_lines = []
        
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                # Get pixel values
                b, g, r = processed_frame[y, x]
                
                # Calculate brightness
                brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
                
                # Get ASCII character
                ascii_char = self.pixel_to_ascii(brightness)
                
                # Add color
                color_code = self.rgb_to_ansi(r, g, b)
                line += f"{color_code}{ascii_char}"
            
            # Reset color at end of line
            line += "\033[0m"
            ascii_lines.append(line)
        
        return "\n".join(ascii_lines)