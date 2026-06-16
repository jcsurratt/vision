# Raspberry Pi Setup Guide

This guide prepares a fresh Raspberry Pi OS install for the Python webcam AI apps in this project.

The project was originally written for Raspberry Pi 4, but these steps also work for Raspberry Pi 5. For Raspberry Pi 5, use the official 27W USB-C power supply if possible, especially when using a USB webcam, keyboard, and mouse.

## 1. Recommended Starting Point

Use:

- Raspberry Pi OS 64-bit with desktop
- Raspberry Pi 4 or Raspberry Pi 5
- USB webcam
- Monitor, keyboard, and mouse
- Internet connection during setup

Do not use Raspberry Pi OS Lite for the normal camp setup. These programs open camera preview windows, so the desktop version is much easier.

## 2. First Boot Checklist

On first boot, complete the Raspberry Pi OS setup wizard:

1. Set the username and password.
2. Connect to Wi-Fi or Ethernet.
3. Set the locale, keyboard, and timezone.
4. Let Raspberry Pi OS update if prompted.
5. Reboot when asked.

If you are using Raspberry Pi Imager before first boot, you can preconfigure the username, Wi-Fi, locale, hostname, and SSH settings there.

## 3. Update Raspberry Pi OS

Open Terminal and run:

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

After the Pi restarts, open Terminal again.

## 4. Install System Packages

Install Python, OpenCV support, camera tools, and helpful diagnostics:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip libatlas-base-dev libopencv-dev v4l-utils fswebcam
```

Add your user to the `video` group so Python/OpenCV can access camera devices:

```bash
sudo usermod -a -G video $USER
sudo reboot
```

After rebooting, log back in.

## 5. Check the Webcam

Plug in the USB webcam.

List detected video devices:

```bash
ls /dev/video*
```

Show webcam details:

```bash
v4l2-ctl --list-devices
```

Optional still-image test:

```bash
fswebcam test.jpg
```

If `test.jpg` is created, the webcam is visible to the Pi.

## 6. Get the Project Files Onto the Pi

Put this project folder somewhere easy to find, such as your home directory.

If you are copying the folder from another computer, the final folder should contain files like:

```text
camera_test.py
object_detector.py
rock_paper_scissors_ai.py
requirements.txt
models/
```

Then open Terminal in the project folder.

For example, if the folder is in your home directory:

```bash
cd ~/image-recognize
```

If the folder has a different name, use that folder name instead.

## 7. Create the Python Virtual Environment

Create the virtual environment on the Raspberry Pi itself. Do not copy a `.venv` folder from Windows or another computer because virtual environments are tied to the operating system and Python install that created them.

From inside the project folder, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

When the virtual environment is active, your Terminal prompt usually starts with:

```text
(.venv)
```

Each time you open a new Terminal and want to run the app, activate the environment again:

```bash
cd ~/image-recognize
source .venv/bin/activate
```

The `.venv` folder is intentionally ignored by Git. Each Raspberry Pi should create its own `.venv` with the commands above.

## 8. Confirm Python Packages Installed

With the virtual environment active, run:

```bash
python3 -c "import cv2; print('OpenCV OK')"
python3 -c "import mediapipe; print('MediaPipe OK')"
python3 -c "import numpy; print('NumPy OK')"
python3 -c "import tflite_runtime; print('TensorFlow Lite Runtime OK')"
```

If one of these commands fails, reinstall the project requirements:

```bash
python3 -m pip install -r requirements.txt
```

## 9. Add TensorFlow Lite Model Files

The object detector needs two files in the `models` folder:

```text
models/detect.tflite
models/labelmap.txt
```

Use a COCO object detection TensorFlow Lite model. The label file should contain one label per line.

Check that the files are present:

```bash
ls models
```

You should see:

```text
detect.tflite
labelmap.txt
```

## 10. Run the Camera Test

With the virtual environment active:

```bash
python3 camera_test.py
```

Expected result:

- A camera preview window opens.
- Press `q` to quit.

If the camera does not open, edit `CAMERA_NUMBER` near the top of `camera_test.py` and try changing it from `0` to `1`.

## 11. Run the Rock Paper Scissors App

With the virtual environment active:

```bash
python3 rock_paper_scissors_ai.py
```

Controls:

- Press `space` to start a round.
- Show Rock, Paper, or Scissors to the camera.
- Press `r` to reset the score.
- Press `q` to quit.

## 12. Run the Object Detector

Make sure the model files are present first:

```bash
ls models
```

Then run:

```bash
python3 object_detector.py
```

Controls:

- Press `q` to quit.

The app should draw boxes around recognized objects. If an object in `TARGET_OBJECTS` is detected, the screen will show `TARGET FOUND!`.

## 13. Visual Studio Code Setup

Install Visual Studio Code if it is not already installed:

```bash
sudo apt update
sudo apt install -y code
code --install-extension ms-python.python
```

Open the project folder in Visual Studio Code:

```bash
cd ~/image-recognize
code .
```

The last command installs the Microsoft Python extension. If it does not install from Terminal, install the extension from the Extensions panel inside Visual Studio Code.

Make sure Visual Studio Code uses the project's virtual environment:

1. Open the Command Palette with `Ctrl+Shift+P`.
2. Search for `Python: Select Interpreter`.
3. Choose the Python inside this project's `.venv` folder.

The path usually looks like:

```text
/home/pi/image-recognize/.venv/bin/python
```

If your project folder has a different name or location, adjust the path.

To run a program from Visual Studio Code:

1. Open the integrated terminal from `Terminal` > `New Terminal`.
2. Activate the virtual environment.
3. Run the Python file.

```bash
source .venv/bin/activate
python3 camera_test.py
```

## 14. Raspberry Pi 5 Notes

For Raspberry Pi 5:

- Use a 5V 5A USB-C power supply when possible.
- A 5V 3A supply may limit USB peripheral power.
- Use a fan or active cooler for longer sessions.
- If the webcam is unreliable, try a powered USB hub.

The Python commands are otherwise the same as Raspberry Pi 4.

## 15. Troubleshooting

### Webcam does not open

Check the camera is detected:

```bash
ls /dev/video*
v4l2-ctl --list-devices
```

Try a different USB port.

Try changing `CAMERA_NUMBER` from `0` to `1` in the Python file.

Make sure your user is in the `video` group:

```bash
groups
```

If `video` is missing:

```bash
sudo usermod -a -G video $USER
sudo reboot
```

### `ModuleNotFoundError: No module named cv2`

Activate the virtual environment and reinstall requirements:

```bash
cd ~/image-recognize
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named mediapipe`

Confirm you are using Raspberry Pi OS 64-bit and that the virtual environment is active:

```bash
uname -m
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

On 64-bit Raspberry Pi OS, `uname -m` should usually show:

```text
aarch64
```

### `ModuleNotFoundError: No module named tflite_runtime`

Activate the virtual environment and reinstall requirements:

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

If the package is unavailable for your Raspberry Pi OS/Python version, you may need to use a compatible Raspberry Pi OS image or install a compatible TensorFlow Lite runtime package.

### Object detector says model files are missing

Confirm these exact files exist:

```bash
ls models
```

Required files:

```text
models/detect.tflite
models/labelmap.txt
```

### Video is slow

Try these changes:

- Lower `FRAME_WIDTH` and `FRAME_HEIGHT` in the Python files.
- Increase `MIN_CONFIDENCE` in `object_detector.py`.
- Use good lighting.
- Keep only one hand in view for Rock Paper Scissors.
- Close extra programs.
- Use active cooling on Raspberry Pi 5.

## 16. Quick Full Command List

Use this section when setting up a Pi from scratch after the first boot wizard.

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

After reboot:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip libatlas-base-dev libopencv-dev v4l-utils fswebcam
sudo apt install -y code
code --install-extension ms-python.python
sudo usermod -a -G video $USER
sudo reboot
```

After reboot:

```bash
cd ~/image-recognize
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
ls /dev/video*
v4l2-ctl --list-devices
python3 camera_test.py
python3 rock_paper_scissors_ai.py
python3 object_detector.py
```
