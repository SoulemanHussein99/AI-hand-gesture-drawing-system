# AI Hand Gesture Drawing System

A real-time computer vision project that enables users to draw, move, and manipulate digital strokes using only hand gestures.

Built using MediaPipe for hand tracking and OpenCV for rendering, this project demonstrates human-computer interaction through AI.

---

## Features

- Real-time hand tracking using MediaPipe
- Gesture-based drawing system
- Smooth cursor movement with filtering (alpha smoothing)
- Multi-finger gesture recognition
- Draw dynamic glowing brush strokes
- Select and move drawn lines
- Clear canvas using gestures
- Interactive real-time canvas system

---

## How It Works

1. Capture video from webcam
2. Detect hand landmarks using MediaPipe
3. Extract key finger positions (index, thumb, etc.)
4. Recognize gestures based on finger states
5. Enable modes:
   - Draw Mode
   - Move Mode
   - Select Mode
   - Clear Canvas
6. Render strokes in real-time using OpenCV

---

## Gesture Controls

- Index + Middle finger close together → drawing mode
- Index finger movement → Draw strokes
- Three fingers extended + thumb/index close → Select line
- All fingers closed (fist) → clear canvas
- Selected line + movement gesture → Move stroke

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Real-time video processing

