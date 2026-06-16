"""
Simple webcam test for Raspberry Pi camp.

Run with:
    python3 camera_test.py

Press q to quit.
"""

import cv2


# =========================
# STUDENT SETTINGS
# =========================

# Most USB webcams are camera 0. Try 1 if your camera does not open.
CAMERA_NUMBER = 0

# Size of the camera picture.
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Name shown at the top of the camera window.
WINDOW_NAME = "Camera Test"


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


def main():
    print("Starting camera test...")
    print("Press q in the camera window to quit.")

    camera = open_camera()
    if camera is None:
        return

    while True:
        success, frame = camera.read()

        if not success:
            print("ERROR: The webcam opened, but no picture was received.")
            break

        cv2.putText(
            frame,
            "Camera test: press q to quit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
    print("Camera test finished.")


if __name__ == "__main__":
    main()
