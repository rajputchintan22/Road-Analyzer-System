from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import numpy as np

from PIL import Image

import tensorflow as tf  # TF2


def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


input_mean = 127.5
input_std = 127.5

interpreter = tf.lite.Interpreter(model_path="model\\opti.lite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

    # check the type of the input tensor
floating_model = input_details[0]['dtype'] == np.float32

    # NxHxWxC, H:1, W:2
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
for i in os.listdir("temp"):
    img = Image.open("temp\\"+i).resize((width, height))

    # add N dim
    input_data = np.expand_dims(img, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels("model\\retrained_labels.txt")

    file_name = i
    path = "temp2"
    template = "{} (score={:0.5f})"
        # for i in top_k:
        #  print(template.format(labels[i], results[i]))
    fp = open(path + '\my_final.csv', 'a')
    temp2 = file_name.replace(".jpg", '')
        #temp2 = temp2.replace(path + "\Final_With_Sides\\", '')
    if results[0] > results[1]:
        print(labels[0])
        temp_string = temp2 + "," + labels[0] + "\n"
        fp.write(temp_string)
    else:
        print(labels[1])
        temp_string = temp2 + "," + labels[1] + "\n"
        fp.write(temp_string)
    fp.close()
