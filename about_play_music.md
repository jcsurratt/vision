# About play_music.py

`play_music.py` is a small MP3 playback demo. It uses `pygame` to load and play an audio file from this project folder.

## What It Does

- Checks that the selected MP3 file exists.
- Starts the `pygame` audio mixer.
- Plays the MP3 file.
- Keeps running until the audio finishes.
- Cleans up the audio mixer before exiting.

By default, the script plays:

```text
winner.mp3
```

## How To Run It

Activate the virtual environment first:

```bash
source .venv/bin/activate
python3 play_music.py
```

On Windows PowerShell, activate the local environment with:

```powershell
.\.venv\Scripts\Activate.ps1
python play_music.py
```

## How To Change The Sound

Near the bottom of the file, change this line:

```python
AUDIO_FILE = "winner.mp3"
```

Examples:

```python
AUDIO_FILE = "loser.mp3"
```

```python
AUDIO_FILE = "sounds/my_sound.mp3"
```

## Required Files

The project currently includes:

```text
winner.mp3
loser.mp3
```

If the MP3 file is missing, the program prints an error and stops.

## Troubleshooting

If no sound plays, check that speakers or headphones are connected and the system volume is turned up.

On Raspberry Pi, test audio with:

```bash
speaker-test -t wav -c 2
```

If Python says `No module named pygame`, reinstall the project packages:

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt --extra-index-url https://google.github.io/mediapipe/getting_started/python.html
```
