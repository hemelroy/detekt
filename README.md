# detekt - AI Based Object and Motion Detector
Detekt is designed to be a neighborhood security camera application. This app will continuously watch for motion. Upon picking up something, it will capture an image and a trained neural network model will classify whether it is a person or some other neighborhood object (dog, package, squirrel, etc.) and store all relevant data within an sqlite database.

- Conducted video/image processing conducted using OpenCV for motion detection, image capture and manipulation
- Trained a region-based convolutional neural network using Tensorflow and Tensorflow model zoo
- Developed a graphical user interface with sqlite database for storing and accessing saved data using SQL and PyQT5
- Performed data processing and summarization of object detection history within a web based time plot using Pandas and Bokeh

## Dependencies
- OpenCV
- Sqlite
- Tensorflow
- Numpy
- Pandas

## Project Overview
This neural network model uses Faster-RCNN, Inception V2 architecture and Tensorflow 1.15. It is based on a modified implementation of such model created by tensorflow found [here](https://github.com/tensorflow/models/tree/master/research/object_detection)

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
