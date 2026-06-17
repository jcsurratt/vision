# Raspberry Pi Webcam AI Camp

Welcome! In this project you will use a Raspberry Pi, a USB webcam, audio, and Python to build computer vision and sound demos:

1. A webcam object detector
2. A Rock Paper Scissors game that watches your hand
3. A simple MP3 player
4. A text-to-speech demo

You do not need to be an expert coder. The programs are written so you can run them first, then experiment by changing a few clearly labeled settings near the top of each file.

## What You Need

- Raspberry Pi 4 or Raspberry Pi 5
- Raspberry Pi OS
- USB webcam
- Speakers or headphones
- Monitor
- Keyboard
- Mouse
- Internet connection for setup

## 1. Assemble Your Raspberry Pi

1. Plug the monitor into the Raspberry Pi.
2. Plug in the keyboard and mouse.
3. Plug in the USB webcam.
4. Connect speakers or headphones if you want to use the audio demos.
5. Connect power to the Raspberry Pi.
6. Wait for Raspberry Pi OS to start.

## 2. Open This Project Folder

Open the folder that contains these files:

- `camera_test.py`
- `object_detector.py`
- `play_music.py`
- `rock_paper_scissors_ai.py`
- `text_to_speech.py`
- `requirements.txt`
- `models/`
- `winner.mp3`
- `loser.mp3`

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

## 7. Play an MP3

Run:

```bash
python3 play_music.py
```

The script plays `winner.mp3` by default. To play another file, change `AUDIO_FILE` near the bottom of `play_music.py`.

## 8. Try Text To Speech

Run:

```bash
python3 text_to_speech.py
```

Type a sentence and press `Enter`. The script uses Google Text-to-Speech, so the Raspberry Pi needs an internet connection.

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

In `play_music.py`, you can change:

- `AUDIO_FILE`

In `text_to_speech.py`, you can change:

- The text typed when the program asks what to say
- The `lang` value passed to `speak_text`

Try changing one setting at a time. Run the program again and see what happens.

## More Details

- [about_object_detector.md](about_object_detector.md)
- [about_play_music.md](about_play_music.md)
- [about_rock_paper_scissors.md](about_rock_paper_scissors.md)
- [about_text_to_speech.md](about_text_to_speech.md)

## Visual Studio Code Tip

If you use Visual Studio Code, make sure it is using the Python inside `.venv`.

Open the project folder in Visual Studio Code, then choose the interpreter at:

```text
.venv/bin/python
```

Ask your instructor to help choose the interpreter if imports like `cv2` or `mediapipe` are not found.
