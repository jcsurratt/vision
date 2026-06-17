# Instructor Setup Guide

This guide is for preparing Raspberry Pi 4 computers for the webcam AI camp project.

## Recommended Hardware

- Raspberry Pi 4
- Raspberry Pi OS, 64-bit recommended
- USB webcam
- Monitor, keyboard, mouse
- Reliable power supply

## System Packages

Open a Terminal and update the Pi:

```bash
sudo apt update
sudo apt upgrade -y
```

Install useful Python and camera dependencies:

```bash
sudo apt install -y python3-venv python3-pip libopenblas-dev libopencv-dev v4l-utils fswebcam unzip wget curl git
```

## Create the Virtual Environment

On Raspberry Pi OS based on Debian Trixie, use Python 3.12 through `pyenv`. Trixie defaults to Python 3.13, which does not work cleanly with MediaPipe on Raspberry Pi ARM64.

Install build tools and `pyenv`:

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv install 3.12
```

From the project folder:

```bash
deactivate 2>/dev/null
rm -rf .venv
~/.pyenv/versions/3.12.*/bin/python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt --extra-index-url https://google.github.io/mediapipe/getting_started/python.html
```

If MediaPipe installation is slow or unavailable on your Raspberry Pi OS image, install packages ahead of camp and test on the exact Pi image students will use.

## TensorFlow Lite Model Files

Place these files in the `models` folder:

```text
models/detect.tflite
models/labelmap.txt
```

Use a COCO object detection TensorFlow Lite model. The label file should contain one label per line.

Download a starter model:

```bash
mkdir -p models
wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
unzip -j coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip "detect.tflite" -d models/
wget -O models/labelmap.txt https://raw.githubusercontent.com/JerryKurata/TFlite-object-detection/main/labelmap.txt
rm coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
```

## Test the Webcam

With the virtual environment active:

```bash
python3 camera_test.py
```

Expected result:

- A webcam preview opens.
- Pressing `q` closes the window.

## Test Object Detection

Make sure `models/detect.tflite` and `models/labelmap.txt` exist, then run:

```bash
python3 object_detector.py
```

Expected result:

- The webcam opens.
- Boxes appear around detected COCO objects.
- `TARGET FOUND!` appears when an item from `TARGET_OBJECTS` is detected.

## Test Rock Paper Scissors

Run:

```bash
python3 rock_paper_scissors_ai.py
```

Expected result:

- The webcam opens.
- One hand is tracked.
- Pressing `space` starts a countdown.
- The program classifies Rock, Paper, or Scissors and updates the score.

## Visual Studio Code Setup

Install Visual Studio Code if it is not already installed:

```bash
sudo apt update
sudo apt install -y code
code --install-extension ms-python.python
```

Open the project folder in Visual Studio Code:

```bash
cd /home/pi/path-to-project
code .
```

The last command installs the Microsoft Python extension. If it does not install from Terminal, install the extension from the Extensions panel inside Visual Studio Code.

To use Visual Studio Code with the virtual environment:

1. Open the Command Palette with `Ctrl+Shift+P`.
2. Search for `Python: Select Interpreter`.
3. Choose the Python inside this project's `.venv` folder.

The path usually looks like:

```text
/home/pi/path-to-project/.venv/bin/python
```

Use the integrated terminal in Visual Studio Code to run the apps:

```bash
source .venv/bin/activate
python3 camera_test.py
```

## Troubleshooting

### Webcam does not open

- Check that the USB webcam is plugged in.
- Try a different USB port.
- Close other programs that might be using the camera.
- Change `CAMERA_NUMBER` from `0` to `1` near the top of the Python file.
- Test the camera with:

```bash
ls /dev/video*
```

### `ModuleNotFoundError: No module named cv2`

The virtual environment may not be active, or requirements were not installed.

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt --extra-index-url https://google.github.io/mediapipe/getting_started/python.html
```

### `ModuleNotFoundError: No module named mediapipe`

MediaPipe may not have installed correctly for the Pi image or Python version. Confirm the Raspberry Pi OS architecture and Python version, then reinstall inside the virtual environment.

```bash
python3 --version
uname -m
source .venv/bin/activate
python3 -m pip install -r requirements.txt --extra-index-url https://google.github.io/mediapipe/getting_started/python.html
```

On Raspberry Pi OS Trixie, use the `pyenv` Python 3.12 setup above instead of the system Python 3.13.

### `ModuleNotFoundError: No module named tensorflow`

The object detector uses `tensorflow-cpu` as its TensorFlow Lite provider. Reinstall requirements inside the virtual environment:

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt --extra-index-url https://google.github.io/mediapipe/getting_started/python.html
```

### Object detector says model files are missing

Confirm the files are named exactly:

```text
models/detect.tflite
models/labelmap.txt
```

### The video is slow

- Lower `FRAME_WIDTH` and `FRAME_HEIGHT` in the Python files.
- Increase `MIN_CONFIDENCE` in `object_detector.py`.
- Use good lighting.
- Keep only one hand in view for Rock Paper Scissors.
