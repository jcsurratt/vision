# About object_detector.py

This program lets your Raspberry Pi look through a webcam and try to name objects it sees.

That might sound complicated, and honestly, there are some powerful ideas hiding inside it. But you do not have to understand every detail at once. You can start with the big picture, run the program, and then explore one small piece at a time.

That is a real way to learn programming.

## What The Program Does

When you run:

```bash
python3 object_detector.py
```

the program:

1. Opens the webcam.
2. Loads an object detection model.
3. Looks at each camera frame.
4. Tries to find objects it recognizes.
5. Draws boxes around those objects.
6. Shows the object name and confidence score.
7. Displays `TARGET FOUND!` when it sees one of the objects we are especially looking for.

## The Big Picture

Here is the basic idea:

```text
The camera sees a picture.
OpenCV gives that picture to Python.
The object detection model studies the picture.
The model guesses what objects are visible.
Python draws boxes and labels on the screen.
```

The code is just a set of instructions that connects those pieces together.

## If The Code Looks Like A Lot

That is normal.

Object detection uses more moving parts than a tiny beginner program. There is a webcam, a model file, a label file, confidence scores, and drawing boxes on the screen.

You do not need to master all of that at once.

Start by looking for this section:

```python
# STUDENT SETTINGS
```

That section was made for experimenting.

## Things You Can Safely Change

Near the top of the file, you will see:

```python
CAMERA_NUMBER = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
TARGET_OBJECTS = ["person", "cell phone", "bottle"]
MIN_CONFIDENCE = 0.50
SHOW_ONLY_TARGETS = False
```

These are good places to start.

## CAMERA_NUMBER

This chooses which camera to use.

Most USB webcams are camera `0`.

If the camera does not open, try:

```python
CAMERA_NUMBER = 1
```

That is like telling the Raspberry Pi, "Try the next camera instead."

## FRAME_WIDTH And FRAME_HEIGHT

These control the size of the camera image.

The current settings are:

```python
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
```

If the video is slow, you can try a smaller size:

```python
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
```

A smaller image can be easier for the Raspberry Pi to process.

## TARGET_OBJECTS

These are the objects the program is especially watching for:

```python
TARGET_OBJECTS = ["person", "cell phone", "bottle"]
```

If the program sees one of those objects, it shows:

```text
TARGET FOUND!
```

You can change the list.

For example:

```python
TARGET_OBJECTS = ["cup", "chair", "book"]
```

The names must match the names in:

```text
models/labelmap.txt
```

If you spell an object differently from the label file, the program may not treat it as a target.

## MIN_CONFIDENCE

`MIN_CONFIDENCE` controls how sure the model has to be before the program shows a detection.

The current setting is:

```python
MIN_CONFIDENCE = 0.50
```

That means the model needs to be at least 50 percent confident.

If you want to see more boxes, try:

```python
MIN_CONFIDENCE = 0.30
```

If you want fewer boxes and only stronger guesses, try:

```python
MIN_CONFIDENCE = 0.70
```

There is a tradeoff:

- Lower confidence shows more guesses, but some may be wrong.
- Higher confidence shows fewer guesses, but they are usually more reliable.

## SHOW_ONLY_TARGETS

This setting controls whether the program shows every object it recognizes or only the target objects.

```python
SHOW_ONLY_TARGETS = False
```

With `False`, the program can draw boxes around many recognized objects.

If you change it to:

```python
SHOW_ONLY_TARGETS = True
```

the program only draws boxes around objects listed in `TARGET_OBJECTS`.

## The Tools Helping Us

This program uses a few Python libraries. A library is code someone else wrote so we can use it in our own project.

That means we get to build something interesting without writing every single part ourselves.

## OpenCV

OpenCV handles the webcam and the video window.

It helps the program:

- Open the camera.
- Read pictures from the camera.
- Draw boxes.
- Draw text.
- Show the video window.
- Notice when you press `q` to quit.

A real-world way to think about OpenCV:

OpenCV is like the camera crew and the screen. It gets the video, puts it where Python can use it, and shows the results back to you.

## NumPy

NumPy helps Python work with image data.

A camera image is really a big grid of numbers. Each pixel has numbers for color.

NumPy helps Python organize and reshape those numbers so the model can understand them.

A real-world way to think about NumPy:

Imagine a huge spreadsheet where every cell contains color information. NumPy helps Python handle that spreadsheet quickly.

## LiteRT

LiteRT is the tool that runs the object detection model.

The model file is:

```text
models/detect.tflite
```

That file contains the trained object detector. The Python code does not learn from scratch while you are using it. The model has already been trained before the program runs.

A real-world way to think about the model:

Imagine someone studied thousands of pictures ahead of time and made a set of instructions for recognizing common objects. LiteRT helps the Raspberry Pi use those instructions.

## The Label File

The label file is:

```text
models/labelmap.txt
```

It contains the object names the model can recognize.

The model might return something like:

```text
class 44
```

The label file helps the program turn that number into a readable name, like:

```text
bottle
```

## What The Boxes Mean

When the program recognizes an object, it draws a box around it.

That box is the model saying:

```text
I think the object is here.
```

The label above the box is the model saying:

```text
I think this object is a bottle.
```

The percentage is the model saying:

```text
I am this confident about my guess.
```

## If The Program Does Not Recognize An Object

That does not mean you did anything wrong.

Object detection models are powerful, but they are not perfect. They can miss objects, guess the wrong label, or feel unsure.

Try this:

- Hold the object closer to the camera.
- Move the object farther from the camera if it is too close.
- Make sure the whole object is visible.
- Use brighter lighting.
- Put the object in front of a plain background.
- Hold the object still.
- Try a different angle.
- Make sure the object is one the model actually knows.
- Lower `MIN_CONFIDENCE` a little.

For example:

```python
MIN_CONFIDENCE = 0.30
```

That may show more guesses, which can help you see what the model is thinking.

## If The Program Guesses Wrong

This can happen.

For example, a model might confuse:

- A cup and a bottle
- A phone and a remote
- A chair and a couch
- A backpack and a handbag

The model is making its best guess from the camera image. If the picture is blurry, dark, crowded, or partly hidden, the guess gets harder.

## If You Do Not See Any Boxes

Try these checks:

1. Make sure the camera window is open.
2. Put a common object in front of the camera.
3. Use good lighting.
4. Check that `MIN_CONFIDENCE` is not too high.
5. Check that `SHOW_ONLY_TARGETS` is not hiding non-target objects.
6. Make sure the model files are in the right folder.

The model files should be:

```text
models/detect.tflite
models/labelmap.txt
```

## If TARGET FOUND Does Not Appear

The program only shows `TARGET FOUND!` when it sees one of the names in `TARGET_OBJECTS`.

Check this list:

```python
TARGET_OBJECTS = ["person", "cell phone", "bottle"]
```

Then check the label file:

```text
models/labelmap.txt
```

The names need to match.

For example, if the label file says:

```text
cell phone
```

then this works:

```python
TARGET_OBJECTS = ["cell phone"]
```

But this may not work:

```python
TARGET_OBJECTS = ["phone"]
```

because `phone` and `cell phone` are not exactly the same text.

## What Happens When You Press q

The program keeps looking through the webcam until you press:

```text
q
```

Then it closes the camera and the video window.

That cleanup matters. It lets the camera be used by another program later.

## Things To Try

Try one small experiment at a time:

- Change `TARGET_OBJECTS`.
- Lower `MIN_CONFIDENCE`.
- Raise `MIN_CONFIDENCE`.
- Turn `SHOW_ONLY_TARGETS` on.
- Change the camera size.
- Try detecting objects in brighter and darker lighting.
- Try a plain background.
- Test which objects the model recognizes best.
- Change the text color or box color.
- Add a sound when `TARGET FOUND!` appears.

Pick one that sounds interesting. You do not have to do everything.

## If Something Breaks

Something breaking does not mean you failed.

It means the computer reached a line it could not understand or found something missing.

Try this:

1. Read the error message.
2. Look at the last thing you changed.
3. Check the file names.
4. Check that the virtual environment is active.
5. Change one small thing and run it again.

That is debugging.

Debugging is not separate from programming. It is part of programming.

## You Are Building Something Real

This project uses the same basic ideas found in real object detection systems:

- A camera collects images.
- A model looks for patterns.
- Code decides what to do with the results.
- The screen shows useful feedback.

You are not just running a toy program. You are working with the same kind of building blocks used in security cameras, self-checkout systems, robots, accessibility tools, and smart devices.

Start small. Try things. Let yourself be curious.
