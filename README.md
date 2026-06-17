# Raspberry Pi Webcam AI Camp

Welcome! In this project you will use a Raspberry Pi 4, a USB webcam, and Python to build two computer vision demos:

1. A webcam object detector
2. A Rock Paper Scissors game that watches your hand

You do not need to be an expert coder. The programs are written so you can run them first, then experiment by changing a few clearly labeled settings near the top of each file.

## What You Need

- Raspberry Pi 4
- Raspberry Pi OS
- USB webcam
- Monitor
- Keyboard
- Mouse
- Internet connection for setup

## 1. Assemble Your Raspberry Pi

1. Plug the monitor into the Raspberry Pi.
2. Plug in the keyboard and mouse.
3. Plug in the USB webcam.
4. Connect power to the Raspberry Pi.
5. Wait for Raspberry Pi OS to start.

## 2. Open This Project Folder

Open the folder that contains these files:

- `camera_test.py`
- `object_detector.py`
- `rock_paper_scissors_ai.py`
- `requirements.txt`
- `models/`

You can run the programs from Visual Studio Code or from the Terminal.

## 3. Create and Use a Virtual Environment

A virtual environment, or `venv`, keeps this project's Python packages together.

On Raspberry Pi OS based on Debian Trixie, use the detailed [Raspberry Pi setup guide](pi_setup.md). Trixie uses Python 3.13 by default, but MediaPipe needs a Python 3.12 virtual environment on the Pi.

Open a Terminal in this project folder and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt --extra-index-url https://google.github.io/mediapipe/getting_started/python.html
```

When the virtual environment is active, your Terminal prompt usually starts with `(.venv)`.

## 4. Test the Webcam

Run:

```bash
python3 camera_test.py
```

A camera window should open.

- Press `q` to quit.
- If the camera does not open, ask your instructor for help.

## 5. Run the Object Detector

Before this program works, your instructor must place these files in the `models` folder:

- `models/detect.tflite`
- `models/labelmap.txt`

Then run:

```bash
python3 object_detector.py
```

The program will draw boxes around objects it recognizes.

- Press `q` to quit.
- If one of your target objects appears, the screen will say `TARGET FOUND!`.

## 6. Run Rock Paper Scissors AI

Run:

```bash
python3 rock_paper_scissors_ai.py
```

How to play:

- Hold one hand in front of the camera.
- Press `space` to start a round.
- Make Rock, Paper, or Scissors before the countdown ends.
- Press `r` to reset the score.
- Press `q` to quit.

## Safe Things To Change

Look near the top of each Python file for a section labeled `STUDENT SETTINGS`.

In `camera_test.py`, you can change:

- `CAMERA_NUMBER`
- `WINDOW_NAME`

In `object_detector.py`, you can change:

- `TARGET_OBJECTS`
- `MIN_CONFIDENCE`
- `SHOW_ONLY_TARGETS`
- `CAMERA_NUMBER`

In `rock_paper_scissors_ai.py`, you can change:

- `WINNING_SCORE`
- `COUNTDOWN_SECONDS`
- `AI_NAMES`
- `CAMERA_NUMBER`

Try changing one setting at a time. Run the program again and see what happens.

## Visual Studio Code Tip

If you use Visual Studio Code, make sure it is using the Python inside `.venv`.

Open the project folder in Visual Studio Code, then choose the interpreter at:

```text
.venv/bin/python
```

Ask your instructor to help choose the interpreter if imports like `cv2` or `mediapipe` are not found.
