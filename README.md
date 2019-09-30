# detekt

## Dependencies
- OpenCV
- Sqlite
- Tensorflow
- Numpy
- Pandas

## Project Overview
This project is built using Tensorflow, and Tensorflow detection model zoo. As such, any files that are not mentioned below do not belong to me, and can be found [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)

Main Program Structure:
- Folders
  - csvs: contains csv files for object detection history
  - inference_graph: contains my final convolutional neural network model trained model
  - images: local storage of images are kept in this folder
  

- Files:
   - main.py: run this to start the application and bring up GUI
   - custom_video_detect.py: used to run model via webcam and detect and record any motion that occurs while simultaneously performing object classification 
   - custom_image_detect: post-processing of information recorded from webcam and application of object detection CNN model on images taken
   - viewImagewindow: use of multiple application windows for webcam views and GUI
   - records.db: sqlite database file, used to store information regarding detected objects and timeframes
