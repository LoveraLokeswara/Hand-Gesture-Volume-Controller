# Hand Gesture Volume Controller 🎵✋

Control your system volume using hand gestures! This project uses OpenCV and MediaPipe to track your hand and adjust the volume based on the distance between your thumb and index finger.

## Features

- 🖐️ Real-time hand tracking using MediaPipe
- 🎚️ Control volume by pinching thumb and index finger
- 📊 Visual feedback with volume bar and percentage
- 🖥️ Cross-platform support (macOS, Windows, Linux)
- 🎥 Live camera feed with hand landmark visualization

## Demo

Simply show your hand to the camera and:
- **Pinch** your thumb and index finger together to **decrease** volume
- **Move them apart** to **increase** volume

## Requirements

- Python 3.7+
- Webcam
- Operating System: macOS, Windows, or Linux

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Hand-Gesture-Volume-Controller.git
cd Hand-Gesture-Volume-Controller
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Platform-Specific Notes

**macOS**: No additional setup required. Uses AppleScript for volume control.

**Windows**: Requires `pycaw` library (included in requirements.txt).

**Linux**: Requires `amixer` (usually pre-installed). If not available:
```bash
sudo apt-get install alsa-utils
```

## Usage

Run the application:
```bash
python main.py
```

### Controls

- Show your hand to the camera (palm facing the camera works best)
- Pinch your thumb and index finger to control volume
- Press **'q'** to quit the application

## How It Works

1. **Hand Detection**: MediaPipe detects and tracks 21 hand landmarks in real-time
2. **Gesture Recognition**: Calculates the distance between thumb tip (landmark 4) and index finger tip (landmark 8)
3. **Volume Mapping**: Maps the distance (30-200 pixels) to volume level (0-100%)
4. **System Control**: Adjusts system volume using platform-specific commands

## Technical Details

- **OpenCV**: Captures video feed and handles image processing
- **MediaPipe**: Provides hand tracking and landmark detection
- **NumPy**: Handles numerical operations and interpolation
- **Platform-specific APIs**: 
  - macOS: AppleScript
  - Windows: pycaw (Core Audio API)
  - Linux: amixer (ALSA)

## Troubleshooting

**Camera not working?**
- Check if your webcam is connected and not being used by another application
- Try changing the camera index in `cv2.VideoCapture(0)` to `1` or `2`

**Volume not changing?**
- Make sure you have the necessary permissions for volume control
- On Linux, ensure `amixer` is installed
- On Windows, ensure `pycaw` is properly installed

**Hand not detected?**
- Ensure good lighting conditions
- Keep your hand within the camera frame
- Try adjusting the `min_detection_confidence` parameter

## Customization

You can customize various parameters in the `HandGestureVolumeController` class:

```python
# Adjust detection sensitivity
min_detection_confidence=0.7  # Lower for easier detection
min_tracking_confidence=0.7   # Lower for smoother tracking

# Adjust distance-to-volume mapping
vol_percentage = np.interp(length, [30, 200], [0, 100])
# Change [30, 200] to adjust gesture sensitivity
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) by Google for hand tracking
- [OpenCV](https://opencv.org/) for computer vision capabilities
- [pycaw](https://github.com/AndreMiras/pycaw) for Windows audio control

## Author

Created with ❤️ by Vera

---

**Note**: This project requires camera access. Make sure to grant the necessary permissions when prompted.

