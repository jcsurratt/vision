import os
import time
import pygame


def play_mp3(file_path):
    # Check if the file actually exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return

    # Initialize the pygame mixer
    pygame.mixer.init()

    try:
        print(f"Loading '{file_path}'...")
        pygame.mixer.music.load(file_path)

        print("Playing... Press Ctrl+C to stop.")
        pygame.mixer.music.play()

        # Keep the script running while the music plays
        while pygame.mixer.music.get_busy():
            time.sleep(1)  # Check every second to keep CPU usage low

    except pygame.error as e:
        print(f"Pygame Error: {e}")
    except KeyboardInterrupt:
        print("\nPlayback stopped by user.")
    finally:
        # Clean up and release resources
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        print("Done.")


if __name__ == "__main__":
    # Replace this with the path to your actual MP3 file
    AUDIO_FILE = "winner.mp3"

    play_mp3(AUDIO_FILE)