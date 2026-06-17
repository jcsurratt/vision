import os
import time
from gtts import gTTS
import pygame


def speak_text(text, lang="en"):
    temp_filename = "temp_speech.mp3"

    print("Generating speech...")
    try:
        # 1. Convert the text to speech using Google's API
        tts = gTTS(text=text, lang=lang, slow=False)

        # 2. Save it to a temporary MP3 file
        tts.save(temp_filename)

        # 3. Initialize pygame mixer and play the file
        pygame.mixer.init()
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()

        print(f'Speaking: "{text}"')

        # Keep script alive while the voice is speaking
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # 4. Clean up resources and remove the temp file
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        # Small delay to ensure the file is unlocked by the OS before deleting
        time.sleep(0.5)
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


if __name__ == "__main__":
    # The text you want the AI to read
    # my_string = (
    #     "Hello! I am reading this string using a natural human voice. "
    #     "Python and gTTS make this incredibly easy."
    # )

    my_string = input("Enter the text you want me to say: ")

    speak_text(my_string)