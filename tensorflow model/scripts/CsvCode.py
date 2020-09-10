import tensorflow as tf
import cv2
import os
from PIL import Image
import csv
import numpy as np
from utils import visualization_utils as vis_util
from utils import backbone

execution_path=os.getcwd()
detection_graph, category_index = backbone.set_model('ssd_mobilenet_v1_coco_2018_01_28', 'mscoco_label_map.pbtxt')
is_color_recognition_enabled = 0

row=list()
row.append("ImageName")
row.append("OriginalImage")
row.append("Horizontal_split")
row.append("Vertical_Split")

with open(execution_path+"/data.csv", 'a',newline='') as csvFile:
	writer = csv.writer(csvFile)
	writer.writerow(row)
csvFile.close()

def single_image_object_counting(input_video, detection_graph, category_index, is_color_recognition_enabled):
        with detection_graph.as_default():
            sess=tf.Session(graph=detection_graph)
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')            

        input_frame = cv2.imread(input_video)

        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(input_frame, axis=0)

        # Actual detection.
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})

        # insert information text to video frame
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Visualization of the results of a detection.        
        counter, csv_line, counting_mode = vis_util.visualize_boxes_and_labels_on_single_image_array(1,input_frame,
                                                                                              1,
                                                                                              is_color_recognition_enabled,
                                                                                              np.squeeze(boxes),
                                                                                              np.squeeze(classes).astype(np.int32),
                                                                                              np.squeeze(scores),
                                                                                              category_index,
                                                                                              use_normalized_coordinates=True,
                                                                                              line_thickness=4)
        if(len(counting_mode) == 0):
            cv2.putText(input_frame, "...", (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)                       
        else:
            cv2.putText(input_frame, counting_mode, (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)
        
        #cv2.imshow('tensorflow_object counting_api',input_frame)        
        #cv2.waitKey(0)
        sess.close
        return counting_mode

    
for filename in os.listdir("/Users/mit/Desktop/moblienet/frames"):
	image_obj = Image.open(execution_path+"/frames/"+filename)
	width,height = image_obj.size
	cropped_image_H_1 = image_obj.crop((0, 0, width, height/2))
	cropped_image_H_2 = image_obj.crop((0, height/2, width, height))
	cropped_image_V_1 = image_obj.crop((0, 0, width/2, height))
	cropped_image_V_2 = image_obj.crop((width/2, 0, width, height))
	
	cropped_image_H_1.save('cropped1.jpg')
	cropped_image_H_2.save('cropped2.jpg')
	cropped_image_V_1.save('cropped3.jpg')
	cropped_image_V_2.save('cropped4.jpg')
	
	detections=single_image_object_counting(os.path.join(execution_path+"/frames/"+filename),detection_graph, category_index, is_color_recognition_enabled)
	detectionsh1=single_image_object_counting(os.path.join(execution_path,"cropped1.JPG"),detection_graph, category_index, is_color_recognition_enabled)
	detectionsh2=single_image_object_counting(os.path.join(execution_path,"cropped2.JPG"),detection_graph, category_index, is_color_recognition_enabled)
	detectionsv1=single_image_object_counting(os.path.join(execution_path,"cropped3.JPG"),detection_graph, category_index, is_color_recognition_enabled)
	detectionsv2=single_image_object_counting(os.path.join(execution_path,"cropped4.JPG"),detection_graph, category_index, is_color_recognition_enabled)
	
	
	row.clear()
	row.append(filename)
	row.append(len(detections))
	row.append(len(detectionsh1)+len(detectionsh2))
	row.append(len(detectionsv1)+len(detectionsv2))
	with open(execution_path+"/data.csv", 'a',newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(row)
	csvFile.close()
