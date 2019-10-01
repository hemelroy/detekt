from custom_video_detect import detected_images, csv_name
import dboperations
import os
import cv2
import numpy as np
import tensorflow as tf
import sys

sys.path.append("..")

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

from collections import Counter

global db_properties
db_properties=[] #list used to input database values

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'

file= open("counters.txt","r")
counter_values = file.read()
counter_values = counter_values.split(",")
file.close()
capture_counter=int(counter_values[0])
detect_counter=int(counter_values[1])


for i in range(len(detected_images)):
    
    IMAGE_NAME = detected_images[i][3]

    # Grab path to current working directory
    CWD_PATH = os.getcwd()

    # Path to frozen detection graph .pb file, which contains the model that is used
    # for object detection.
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

    # Path to image
    PATH_TO_IMAGE = os.path.join(CWD_PATH,IMAGE_NAME)

    # Number of classes the object detector can identify
    NUM_CLASSES = 6


    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    # Define input and output tensors (i.e. data) for the object detection classifier

    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Load image using OpenCV and
    # expand image dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    image = cv2.imread(PATH_TO_IMAGE)
    image_expanded = np.expand_dims(image, axis=0)


    
    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    # Draw the results of the detection (aka 'visulaize the results')

    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.60)

    # All the results have been drawn on image. Now display the image.
    cv2.imshow('Object detector', image)
    detect_imgpath = 'images/detectimg' + str(detect_counter) +".png"
    detect_counter+=1
    cv2.imwrite(detect_imgpath, image)

    print([category_index.get(value) for index,value in enumerate(classes[0]) if scores[0,index] > 0.5])
    all_objects = ([category_index.get(value) for index,value in enumerate(classes[0]) if scores[0,index] > 0.5])

    #Iterate through all the objects detected, create a list with names of those objects
    db_objects = []
    num_objects = len(all_objects)
    for j in range(num_objects):
        db_objects.append(all_objects[j]['name'])

    quantities = dict(Counter(db_objects)) #creates a dictionary telling you how many of each class exists in the image
    db_properties.append([detected_images[i][0], detected_images[i][1], detected_images[i][2], detected_images[i][3], detect_imgpath, quantities])
    #imgname, date, time, imgpath, detectimgpath, quantities dictionary

    # Press any key to close the image
    cv2.waitKey(0)

    # Clean up
    cv2.destroyAllWindows()

#Output of a detection from the algorithm: [{'id': 2, 'name': 'cat'}, {'id': 1, 'name': 'dog'}, {'id': 4, 'name': 'squirrel'}]
print(db_properties)

countertext = str(capture_counter) + "," + str(detect_counter)
file= open("counters.txt","w")
file.write(countertext)
file.close()

dboperations.insert_captures(db_properties, csv_name)