import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

import time, pandas
from datetime import datetime

import cv2
cap = cv2.VideoCapture(0)

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")


# ## Object detection imports
# Here are the imports from the object detection module.

from utils import label_map_util

from utils import visualization_utils as vis_util

#Lists for storing db information
global detected_images
detected_images = []

MODEL_NAME = 'inference_graph'


# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

NUM_CLASSES = 6

file= open("counters.txt","r")
counter_values = file.read()
counter_values = counter_values.split(",")
file.close()
capture_counter=int(counter_values[0])
detect_counter=int(counter_values[1])



# ## Load frozen Tensorflow model into memory.

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


#Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


# Detection
PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3) ]

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

frame_counter = 0
in_frame = False 

first_frame = None
status_list = [None, None]
status_times = []
times_df = pandas.DataFrame(columns = ["Start", "End"])


with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    while True:
      ret, image_np = cap.read()

#Motion detection
      frame = image_np 
      status = 0 #Indicator for whether or not object is in frame
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      gray = cv2.GaussianBlur(gray, (21, 21), 0) #smooths image to remove noise and increase accuracy

      if first_frame is None:
        first_frame = gray
        continue

      delta_frame = cv2.absdiff(first_frame, gray)

      thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

      thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

      cnts,_ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1

      status_list.append(status)

    #Only keep relevant status values, prevents running out of memory
      status_list = status_list[-2:]

      if frame_counter >= 10:
            capture_name = "imcapture_{}.png".format(capture_counter)
            path="images"
            cv2.imwrite(os.path.join(path , capture_name), frame)
            print("{} written!".format(capture_name))
            capture_counter += 1
            frame_counter = 0
            in_frame = False
           #Configure image path 
            detect_path=path+"/"+capture_name
           #Configure date 
            detect_date = datetime.now()
            detect_date = detect_date.strftime("%Y-%m-%d")
           #Configure time
            detect_time = datetime.now()
            detect_time = detect_time.strftime("%H:%M:%S")
            detected_images.append([capture_name, detect_date, detect_time, detect_path]) #imagename, date, time, imagepath

      if in_frame == True:
          frame_counter += 1

      if status_list[-1] == 1 and status_list[-2] == 0:
        status_times.append(datetime.now())
        in_frame = True
        if in_frame == True:
            frame_counter +=1
        
      if status_list[-1] == 0 and status_list[-2] == 1:
        status_times.append(datetime.now())
        in_frame = False 
        if in_frame == True:
            frame_counter +=1


      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      image_np_expanded = np.expand_dims(image_np, axis=0)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      # Each box represents a part of the image where a particular object was detected.
      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      # Each score represent how level of confidence for each of the objects.
      # Score is shown on the result image, together with the class label.
      scores = detection_graph.get_tensor_by_name('detection_scores:0')
      classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      # Actual detection.
      (boxes, scores, classes, num_detections) = sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      # Visualization of the results of a detection.
      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)

      cv2.imshow('object detection', cv2.resize(image_np, (800,600)))
      if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

for i in range(0, len(status_times), 2):
    times_df = times_df.append({"Start" : status_times[i], "End" : status_times[i + 1]}, ignore_index=True)

csv_name = datetime.now().strftime("%Y-%m-%d")
csv_name = csv_name + '.csv'

times_df.to_csv(os.path.join('csvs', csv_name))
print("CSV file created")

print(detected_images)

countertext = str(capture_counter) + "," + str(detect_counter)
file= open("counters.txt","w")
file.write(countertext)
file.close()

