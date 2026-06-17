"""
USB webcam object detector for Raspberry Pi camp.

This program uses a TensorFlow Lite object detection model.

Required files:
    models/detect.tflite
    models/labelmap.txt

Run with:
    python3 object_detector.py

Press q to quit.
"""

import os

import cv2
import numpy as np

INTERPRETER_IMPORT_ERRORS = []

try:
    from tflite_runtime.interpreter import Interpreter
except ImportError as error:
    INTERPRETER_IMPORT_ERRORS.append(f"tflite_runtime: {error}")
    try:
        from ai_edge_litert.interpreter import Interpreter
    except ImportError as error:
        INTERPRETER_IMPORT_ERRORS.append(f"ai_edge_litert: {error}")
        try:
            import tensorflow as tf

            Interpreter = tf.lite.Interpreter
        except ImportError as error:
            INTERPRETER_IMPORT_ERRORS.append(f"tensorflow: {error}")
            try:
                from tensorflow.lite.python.interpreter import Interpreter
            except ImportError as error:
                INTERPRETER_IMPORT_ERRORS.append(f"tensorflow.lite.python.interpreter: {error}")
                Interpreter = None
except Exception as error:
    INTERPRETER_IMPORT_ERRORS.append(f"tflite_runtime: {error}")
    try:
        from ai_edge_litert.interpreter import Interpreter
    except Exception as error:
        INTERPRETER_IMPORT_ERRORS.append(f"ai_edge_litert: {error}")
        Interpreter = None


# =========================
# STUDENT SETTINGS
# =========================

# Most USB webcams are camera 0. Try 1 if your camera does not open.
CAMERA_NUMBER = 0

# Size of the camera picture.
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Objects we are especially looking for.
# These names must match labels in models/labelmap.txt.
TARGET_OBJECTS = ["person", "cell phone", "bottle"]

# Only show detections at or above this confidence.
# Try 0.30 for more boxes, or 0.70 for fewer boxes.
MIN_CONFIDENCE = 0.50

# If True, only draw boxes around TARGET_OBJECTS.
# If False, draw boxes around every detected object.
SHOW_ONLY_TARGETS = False


# =========================
# MODEL FILES
# =========================

MODEL_PATH = os.path.join("models", "detect.tflite")
LABEL_PATH = os.path.join("models", "labelmap.txt")


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


def load_labels(label_path):
    """Load the object names from the label file."""
    labels = []

    with open(label_path, "r", encoding="utf-8") as label_file:
        for line in label_file:
            label = line.strip()
            if label:
                labels.append(label)

    # Some COCO label files start with ??? as a placeholder.
    if labels and labels[0] == "???":
        labels = labels[1:]

    return labels


def check_model_files():
    """Make sure the model files are present before starting."""
    if Interpreter is None:
        print("ERROR: TensorFlow Lite is not installed.")
        print("The object detector needs the ai-edge-litert package.")
        print("First confirm the Pi copy of requirements.txt includes ai-edge-litert:")
        print("    grep -n . requirements.txt")
        print("Activate the virtual environment and install the requirements:")
        print("    source .venv/bin/activate")
        print(
            "    python3 -m pip install -r requirements.txt "
            "--extra-index-url https://google.github.io/mediapipe/getting_started/python.html"
        )
        print("If ai-edge-litert still does not install, try installing it directly:")
        print("    python3 -m pip install ai-edge-litert")
        print("Import attempts:")
        for import_error in INTERPRETER_IMPORT_ERRORS:
            print("   -", import_error)
        return False

    if not os.path.exists(MODEL_PATH):
        print("ERROR: Missing model file:", MODEL_PATH)
        print("Ask your instructor to place detect.tflite in the models folder.")
        return False

    if not os.path.exists(LABEL_PATH):
        print("ERROR: Missing label file:", LABEL_PATH)
        print("Ask your instructor to place labelmap.txt in the models folder.")
        return False

    return True


def get_output_tensor(interpreter, possible_names, index):
    """Get an output tensor using common TensorFlow Lite output names."""
    output_details = interpreter.get_output_details()

    for detail in output_details:
        name = detail["name"].lower()
        for possible_name in possible_names:
            if possible_name in name:
                return interpreter.get_tensor(detail["index"])[0]

    # If names are different, use the normal COCO model output order.
    return interpreter.get_tensor(output_details[index]["index"])[0]


def prepare_input(frame, input_width, input_height, floating_model):
    """Resize the camera frame so the model can understand it."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized_frame = cv2.resize(rgb_frame, (input_width, input_height))

    input_data = np.expand_dims(resized_frame, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    return input_data


def draw_detection(frame, label, confidence, box):
    """Draw one object box and label on the screen."""
    frame_height, frame_width, _ = frame.shape
    ymin, xmin, ymax, xmax = box

    left = int(xmin * frame_width)
    right = int(xmax * frame_width)
    top = int(ymin * frame_height)
    bottom = int(ymax * frame_height)

    left = max(0, left)
    right = min(frame_width, right)
    top = max(0, top)
    bottom = min(frame_height, bottom)

    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    text = f"{label}: {int(confidence * 100)}%"
    cv2.putText(
        frame,
        text,
        (left, max(25, top - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2,
    )


def show_instructions(frame):
    """Show simple instructions on the camera image."""
    cv2.putText(
        frame,
        "Object Detector - press q to quit",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )


def main():
    print("Starting object detector...")
    print("Press q in the camera window to quit.")

    if not check_model_files():
        return

    labels = load_labels(LABEL_PATH)
    interpreter = Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    input_height = input_details[0]["shape"][1]
    input_width = input_details[0]["shape"][2]
    floating_model = input_details[0]["dtype"] == np.float32

    camera = open_camera()
    if camera is None:
        return

    while True:
        success, frame = camera.read()

        if not success:
            print("ERROR: The webcam opened, but no picture was received.")
            break

        input_data = prepare_input(frame, input_width, input_height, floating_model)
        interpreter.set_tensor(input_details[0]["index"], input_data)
        interpreter.invoke()

        boxes = get_output_tensor(interpreter, ["location"], 0)
        classes = get_output_tensor(interpreter, ["class"], 1)
        scores = get_output_tensor(interpreter, ["score"], 2)

        target_found = False

        for i in range(len(scores)):
            confidence = scores[i]
            if confidence < MIN_CONFIDENCE:
                continue

            class_id = int(classes[i])
            if class_id < 0 or class_id >= len(labels):
                continue

            label = labels[class_id]
            is_target = label in TARGET_OBJECTS

            if is_target:
                target_found = True

            if SHOW_ONLY_TARGETS and not is_target:
                continue

            draw_detection(frame, label, confidence, boxes[i])

        show_instructions(frame)

        if target_found:
            cv2.putText(
                frame,
                "TARGET FOUND!",
                (15, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 255),
                3,
            )

        cv2.imshow("Object Detector", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
    print("Object detector finished.")


if __name__ == "__main__":
    main()
