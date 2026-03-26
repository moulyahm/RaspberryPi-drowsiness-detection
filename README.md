# Drowsiness Detection using Raspberry Pi (LED Alert System)

## Description
This project detects driver drowsiness in real-time using a Raspberry Pi camera and triggers an LED alert when the user appears sleepy.

## Concept
The system uses Eye Aspect Ratio (EAR) calculated from facial landmarks to detect eye closure over time.

## Hardware Used
* Raspberry Pi 4
* Pi Camera / USB Camera
* LED
* Resistor (220Ω)
* Breadboard

## Software Used
* Python 3
* OpenCV
* MediaPipe
* NumPy
* RPi.GPIO

## Installation
```bash
sudo apt update
sudo apt install python3-pip
pip3 install opencv-python mediapipe numpy RPi.GPIO
```

## Run the Project
```bash
python3 src/drowsiness_detection.py
```

## GPIO Connection
* LED → GPIO 23
* GND → Resistor → LED

## Working
* Detects face using MediaPipe Face Mesh
* Extracts eye landmarks
* Calculates Eye Aspect Ratio (EAR)
* If eyes remain closed for a threshold time:

  * LED turns ON
  * Alert message displayed

## Future Improvements
* Add buzzer alert
* Send mobile notification
* Integrate with vehicle system
* Use Edge AI model optimization




