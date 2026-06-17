# Model Files

The instructor must place the TensorFlow Lite COCO object detection files in this folder.

Required files:

```text
detect.tflite
labelmap.txt
```

The object detector expects these paths:

```text
models/detect.tflite
models/labelmap.txt
```

The label file should contain one object label per line.

This folder is only for object detection model files. The audio demo files, such as `winner.mp3` and `loser.mp3`, should stay in the main project folder unless the Python code is changed to point somewhere else.

To download a starter COCO model on the Raspberry Pi, run these commands from the project folder:

```bash
mkdir -p models
wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
unzip -j coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip "detect.tflite" -d models/
wget -O models/labelmap.txt https://raw.githubusercontent.com/JerryKurata/TFlite-object-detection/main/labelmap.txt
rm coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
```
