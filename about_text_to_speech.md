# About text_to_speech.py

`text_to_speech.py` turns typed text into spoken audio. It uses Google Text-to-Speech through `gTTS`, saves the generated speech as a temporary MP3 file, and plays it with `pygame`.

## What It Does

- Asks the user to type text.
- Sends the text to Google Text-to-Speech.
- Saves the generated voice to `temp_speech.mp3`.
- Plays the temporary MP3 file.
- Deletes `temp_speech.mp3` when finished.

## How To Run It

Activate the virtual environment first:

```bash
source .venv/bin/activate
python3 text_to_speech.py
```

On Windows PowerShell, activate the local environment with:

```powershell
.\.venv\Scripts\Activate.ps1
python text_to_speech.py
```

Then type a sentence and press `Enter`.

## Internet Requirement

This script uses Google Text-to-Speech, so it needs an internet connection when generating the speech audio.

To check internet access on Raspberry Pi:

```bash
ping -c 4 google.com
```

## Temporary File

The script creates this file while it is speaking:

```text
temp_speech.mp3
```

The file is deleted automatically after playback. It is also listed in `.gitignore` so it does not get committed if the script is stopped early.

## Changing The Voice Language

The `speak_text` function accepts a language code:

```python
speak_text("Hello", lang="en")
```

For example, Spanish would use:

```python
speak_text("Hola", lang="es")
```

## Troubleshooting

If Python says `No module named gtts` or `No module named pygame`, reinstall the project packages:

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt --extra-index-url https://google.github.io/mediapipe/getting_started/python.html
```

If no sound plays, test the Raspberry Pi audio output:

```bash
speaker-test -t wav -c 2
```
