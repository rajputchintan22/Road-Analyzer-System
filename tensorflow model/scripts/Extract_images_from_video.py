import cv2
import math
import os
videoFile = "D:\Test\Show2\Final.mp4"
imagesFolder = videoFile[:-4]
os.mkdir(imagesFolder)
cap = cv2.VideoCapture(videoFile)
frameRate = 30.00 #frame rate
count = 0
while cap.isOpened():
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if frameId % math.floor(frameRate) == 0:
        filename = imagesFolder + "/" +  str(count) + ".jpg"
        cv2.imwrite(filename, frame)
        count += 1
cap.release()
print("Done!")
