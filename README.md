# 🎨 Colorful ASCII Webcam

**Real-time video to colorful ASCII art converter with selfie capture and recording capabilities**

Transform your webcam feed into stunning ASCII art in real-time! This web application uses your camera to create colorful ASCII representations of your video stream, complete with adjustable settings, selfie capture, and screen recording functionality.

LIVE DEMO AVAILABLE at [https://pragnyanramtha.github.io/ascii-webcam/](https://pragnyanramtha.github.io/ascii-webcam/)

![ASCII Webcam Demo](https://img.shields.io/badge/Demo-Live-brightgreen)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![Canvas API](https://img.shields.io/badge/Canvas_API-FF6B6B?logo=html5&logoColor=white)

## ✨ Features

### 🎥 Real-Time ASCII Conversion
- **Live Processing**: Converts webcam feed to ASCII art at 30+ FPS
- **Colorful Output**: Preserves original colors in ASCII representation
- **Smart Character Mapping**: Uses optimized character set for better visual quality
- **Aspect Ratio Preservation**: Maintains proper video proportions

### 🎛️ Advanced Controls
- **Contrast Adjustment**: Fine-tune image contrast (0.5x - 3.0x)
- **Resolution Control**: 5 quality levels from Very Low to Very High
- **Color Intensity**: Adjust color saturation (0.1x - 2.0x)
- **Real-time FPS Counter**: Monitor performance

### 📸 Capture & Recording
- **ASCII Selfies**: Capture and download your ASCII art as PNG images
- **Screen Recording**: Record your ASCII video feed as WebM files
- **Instant Download**: One-click download for all captures
- **Preview Window**: Live preview of captured selfies

### 🖥️ User Experience
- **Fullscreen Mode**: Immersive viewing experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Sleek cyber-punk inspired interface
- **Real-time Notifications**: Status updates and confirmations

## 🚀 Quick Start

### Option 1: Direct HTML File
1. **Download** the HTML file from this repository
2. **Open** the file in any modern web browser
3. **Allow** camera permissions when prompted
4. **Start creating** ASCII art!

### Option 2: Local Web Server
```bash
# Using Python 3
python -m http.server 8000

# Using Node.js
npx serve .

# Using PHP
php -S localhost:8000
```

Then open `http://localhost:8000` in your browser.

## 🎮 How to Use

### Getting Started
1. **Open** the application in your web browser
2. **Grant** camera permissions when prompted
3. **Watch** as your video feed transforms into colorful ASCII art
4. **Adjust** settings using the control panel

### Taking Selfies
1. **Position** yourself in front of the camera
2. **Click** the "Selfie" button
3. **Preview** appears in the bottom-right corner
4. **Click** "Download" to save your ASCII selfie

### Recording Videos
1. **Click** the "Record" button to start recording
2. **Red indicator** shows recording is active
3. **Click** "Stop" to end recording
4. **Video** automatically downloads as WebM file

### Adjusting Settings
- **Contrast Slider**: Enhance or reduce image contrast
- **Resolution Slider**: Balance between quality and performance
- **Color Intensity**: Make colors more or less vibrant

## 🛠️ Technical Details

### Browser Compatibility
- ✅ **Chrome 88+** (Recommended)
- ✅ **Firefox 85+**
- ✅ **Safari 14+**
- ✅ **Edge 88+**

### Required APIs
- **MediaDevices API**: Camera access
- **Canvas API**: Video processing and ASCII rendering
- **MediaRecorder API**: Screen recording functionality
- **Fullscreen API**: Immersive mode

### Performance
- **Frame Rate**: 30+ FPS on modern devices
- **Resolution**: Adaptive based on device capabilities
- **Memory Usage**: Optimized for continuous operation
- **CPU Usage**: Hardware-accelerated when available

## 🎨 Customization

### Character Set
The application uses an optimized ASCII character set:
```javascript
const charSet = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$";
```

### Color Processing
- **Brightness Calculation**: Uses luminance formula (0.299*R + 0.587*G + 0.114*B)
- **Color Preservation**: Maps original RGB values to ASCII characters
- **Intensity Control**: Multiplier for color saturation

### Resolution Levels
1. **Very Low**: 8% of original resolution
2. **Low**: 13% of original resolution  
3. **Medium**: 18% of original resolution
4. **High**: 23% of original resolution
5. **Very High**: 28% of original resolution

## 🔧 Configuration Options

### Modifying Settings
Edit the `config` object in the JavaScript section:

```javascript
const config = {
    contrast: 1.5,          // Image contrast multiplier
    brightness: 1.2,        // Image brightness multiplier
    resolution: 3,          // Resolution level (1-5)
    colorIntensity: 1.0,    // Color saturation multiplier
    charSet: "...",         // ASCII character set
    frameRate: 0            // Target frame rate (0 = unlimited)
};
```

### Styling Customization
- **Colors**: Modify CSS custom properties
- **Fonts**: Change monospace font family
- **Layout**: Adjust grid system and spacing
- **Animations**: Customize transitions and effects

## 📱 Mobile Support

### Touch Controls
- **Tap to Focus**: Touch controls for better mobile experience
- **Gesture Support**: Pinch-to-zoom and swipe gestures
- **Orientation**: Automatic layout adjustment

### Performance Optimization
- **Reduced Resolution**: Lower default settings for mobile
- **Battery Saving**: Adaptive frame rate based on device
- **Memory Management**: Optimized for mobile browsers

## 🐛 Troubleshooting

### Common Issues

**Camera Not Working**
- Check browser permissions for camera access
- Ensure you're using HTTPS (required for camera API)
- Try refreshing the page and allowing permissions again

**Poor Performance**
- Lower the resolution setting
- Close other browser tabs
- Check if hardware acceleration is enabled

**Recording Not Working**
- Ensure your browser supports MediaRecorder API
- Check available disk space
- Try using Chrome for best recording support

**Colors Look Washed Out**
- Increase color intensity setting
- Adjust contrast for better color definition
- Check your camera's lighting conditions

### Browser-Specific Notes
- **Safari**: May require additional permissions for recording
- **Firefox**: WebM recording format may not be supported on all systems
- **Mobile Browsers**: Limited recording capabilities on some devices

## 🤝 Contributing

### Development Setup
1. **Fork** the repository
2. **Clone** your fork locally
3. **Make** your changes
4. **Test** across different browsers
5. **Submit** a pull request

### Areas for Improvement
- [ ] Add more ASCII character sets
- [ ] Implement edge detection for better detail
- [ ] Add filter effects (sepia, noir, etc.)
- [ ] Optimize for better mobile performance
- [ ] Add audio recording support

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Canvas API**: For powerful 2D graphics capabilities
- **MediaDevices API**: For seamless camera access
- **Font Awesome**: For beautiful icons
- **Modern Web Standards**: Making this possible without plugins

## 📞 Support

If you encounter any issues or have questions:
1. **Check** the troubleshooting section above
2. **Browse** existing issues in the repository
3. **Create** a new issue with detailed information
4. **Include** browser version and error messages

---

**Made with ❤️ for the ASCII art community**

*Transform your world into art, one character at a time!* 🎨✨
