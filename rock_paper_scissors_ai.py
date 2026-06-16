"""
Rock Paper Scissors AI game for Raspberry Pi camp.

This program uses a webcam and MediaPipe Hands to watch one hand.

Run with:
    python3 rock_paper_scissors_ai.py

Controls:
    space = start a round
    r     = reset score
    q     = quit
"""

import random
import time

import cv2
import mediapipe as mp


# =========================
# STUDENT SETTINGS
# =========================

# Most USB webcams are camera 0. Try 1 if your camera does not open.
CAMERA_NUMBER = 0

# Size of the camera picture.
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# First player to reach this score wins the match.
WINNING_SCORE = 5

# Number of seconds before the hand sign is judged.
COUNTDOWN_SECONDS = 3

# The computer will randomly pick one of these names.
AI_NAMES = ["Computer", "Robo Ref", "Pi Champion"]


# =========================
# GAME SETTINGS
# =========================

CHOICES = ["Rock", "Paper", "Scissors"]
WINDOW_NAME = "Rock Paper Scissors AI"


def open_camera():
    """Open the webcam and return it."""
    camera = cv2.VideoCapture(CAMERA_NUMBER)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not camera.isOpened():
        print("ERROR: Could not open the webcam.")
        print("Check that the USB webcam is plugged in.")
        print("If it still does not work, change CAMERA_NUMBER to 1.")
        return None

    return camera


def count_extended_fingers(hand_landmarks):
    """Count fingers that look extended.

    This simple method works best when your palm faces the camera.
    """
    landmarks = hand_landmarks.landmark

    # Fingertip landmarks and the joints below them.
    finger_tips = [8, 12, 16, 20]
    finger_joints = [6, 10, 14, 18]

    extended_fingers = 0

    for tip, joint in zip(finger_tips, finger_joints):
        if landmarks[tip].y < landmarks[joint].y:
            extended_fingers += 1

    return extended_fingers


def classify_gesture(hand_landmarks):
    """Turn a hand shape into Rock, Paper, Scissors, or Unknown."""
    extended_fingers = count_extended_fingers(hand_landmarks)

    if extended_fingers <= 1:
        return "Rock"

    if extended_fingers == 2:
        return "Scissors"

    if extended_fingers >= 4:
        return "Paper"

    return "Unknown"


def choose_winner(player_choice, ai_choice):
    """Decide who won the round."""
    if player_choice == "Unknown":
        return "Show Rock, Paper, or Scissors"

    if player_choice == ai_choice:
        return "Tie"

    if player_choice == "Rock" and ai_choice == "Scissors":
        return "Player"

    if player_choice == "Paper" and ai_choice == "Rock":
        return "Player"

    if player_choice == "Scissors" and ai_choice == "Paper":
        return "Player"

    return "AI"


def add_text(frame, text, x, y, color=(255, 255, 255), size=0.7, thickness=2):
    """Draw readable text on the video frame."""
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)


def draw_game_screen(frame, game_info):
    """Show the game status on the camera image."""
    add_text(frame, "Rock Paper Scissors AI", 15, 30, (0, 255, 255), 0.8, 2)
    add_text(frame, "space: play   r: reset   q: quit", 15, 60)

    add_text(frame, f"AI Name: {game_info['ai_name']}", 15, 100)
    add_text(frame, f"Player Choice: {game_info['player_choice']}", 15, 135)
    add_text(frame, f"AI Choice: {game_info['ai_choice']}", 15, 170)
    add_text(frame, f"Round Winner: {game_info['winner']}", 15, 205)

    score_text = f"Score  Player {game_info['player_score']} - AI {game_info['ai_score']}"
    add_text(frame, score_text, 15, 245, (0, 255, 0), 0.8, 2)

    if game_info["countdown_message"]:
        add_text(frame, game_info["countdown_message"], 15, 295, (0, 255, 255), 1.0, 3)

    if game_info["match_message"]:
        add_text(frame, game_info["match_message"], 15, 345, (0, 255, 255), 0.9, 3)


def update_score(game_info):
    """Add one point to the round winner."""
    if game_info["winner"] == "Player":
        game_info["player_score"] += 1

    if game_info["winner"] == "AI":
        game_info["ai_score"] += 1

    if game_info["player_score"] >= WINNING_SCORE:
        game_info["match_message"] = "Player wins the match! Press r to reset."

    if game_info["ai_score"] >= WINNING_SCORE:
        game_info["match_message"] = "AI wins the match! Press r to reset."


def reset_game(game_info):
    """Reset the score and pick a new AI name."""
    game_info["ai_name"] = random.choice(AI_NAMES)
    game_info["player_score"] = 0
    game_info["ai_score"] = 0
    game_info["player_choice"] = "None yet"
    game_info["ai_choice"] = "None yet"
    game_info["winner"] = "Press space to play"
    game_info["countdown_message"] = ""
    game_info["match_message"] = ""


def create_game_info():
    """Create the starting game information."""
    game_info = {}
    reset_game(game_info)
    return game_info


def main():
    print("Starting Rock Paper Scissors AI...")
    print("Press space to play, r to reset, or q to quit.")

    camera = open_camera()
    if camera is None:
        return

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    game_info = create_game_info()

    round_start_time = None
    round_in_progress = False
    current_gesture = "Unknown"

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.60,
        min_tracking_confidence=0.60,
    ) as hands:
        while True:
            success, frame = camera.read()

            if not success:
                print("ERROR: The webcam opened, but no picture was received.")
                break

            # Flip the image so it feels like looking in a mirror.
            frame = cv2.flip(frame, 1)

            # MediaPipe uses RGB images, while OpenCV uses BGR images.
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            current_gesture = "Unknown"

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                current_gesture = classify_gesture(hand_landmarks)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if round_in_progress:
                seconds_passed = time.time() - round_start_time
                seconds_left = COUNTDOWN_SECONDS - int(seconds_passed)

                if seconds_left > 0:
                    game_info["countdown_message"] = f"Get ready: {seconds_left}"
                else:
                    game_info["player_choice"] = current_gesture
                    game_info["ai_choice"] = random.choice(CHOICES)
                    game_info["winner"] = choose_winner(
                        game_info["player_choice"],
                        game_info["ai_choice"],
                    )
                    game_info["countdown_message"] = ""
                    update_score(game_info)
                    round_in_progress = False

            draw_game_screen(frame, game_info)
            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == ord("r"):
                print("Resetting the game.")
                reset_game(game_info)
                round_in_progress = False

            if key == ord(" "):
                if game_info["match_message"]:
                    print("The match is over. Press r to reset.")
                elif not round_in_progress:
                    print("Starting a round. Show your hand sign!")
                    game_info["winner"] = "Round in progress"
                    game_info["player_choice"] = "Choosing..."
                    game_info["ai_choice"] = "Choosing..."
                    round_start_time = time.time()
                    round_in_progress = True

    camera.release()
    cv2.destroyAllWindows()
    print("Rock Paper Scissors AI finished.")


if __name__ == "__main__":
    main()
