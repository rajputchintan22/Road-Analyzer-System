from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#import cv2
import math
import os
import shutil
import webbrowser
import numpy as np
from PIL import Image
import csv

import tensorflow as tf  # TF2

def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles



path = "Show2"
'''videoFile = path+"\Final.mp4"
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
cap.release()'''
save_path = path+"\\Final_With_Sides\\"
os.mkdir(save_path)
for filename in os.listdir(path+"\Final"):
    execution_path = path + "\Final\\"
    image_obj = Image.open(execution_path + filename)
    width, height = image_obj.size
    cropped_image_left = image_obj.crop((0, 0, width/3, height))
    cropped_image_center = image_obj.crop((width/3, 0, 2*width/3, height))
    cropped_image_right = image_obj.crop((2*width/3, 0, width, height))
    cropped_image_left.save(save_path+filename[:-4]+'_right_.jpg')
    cropped_image_center.save(save_path+filename[:-4]+'_center_.jpg')
    cropped_image_right.save(save_path+filename[:-4]+'_left_.jpg')

fp = open(path+'\my_final.csv', 'w')
fp.close()
dirName = path +'\Final_With_Sides'
listOfFiles = getListOfFiles(dirName)
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


for i in listOfFiles:
    #os.system("python lite_image_classy.py --model_file=model/opti.lite --label_file=model/retrained_labels.txt --image="+i)

    img = Image.open(i).resize((width, height))

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
    template = "{} (score={:0.5f})"
    # for i in top_k:
    #  print(template.format(labels[i], results[i]))
    fp = open(path + '\my_final.csv', 'a')
    temp2 = file_name.replace(".jpg", '')
    temp2 = temp2.replace(path + "\Final_With_Sides\\", '')
    if results[0] > results[1]:
        temp_string = temp2 + "," + labels[0] + "\n"
        fp.write(temp_string)
    else:
        temp_string = temp2 + "," + labels[1] + "\n"
        fp.write(temp_string)
    fp.close()



fp = open(path + '\\my_final.csv', 'r')
l = fp.readlines()
fp.close()
for i in range(0, len(l)):
    l[i] = l[i].replace('\n','')
l.sort()
final = []
for i in range(0, len(l), 3):
    temp = [0, '', '', '']
    if "good road" in l[i]:
        temp[2] = 'good road'
        l[i] = l[i].replace(',good road', '')
        l[i] = l[i].replace('_center_', '')
        temp[0] = int(l[i])
    else:
        temp[2] = 'bad road'
        l[i] = l[i].replace(',bad road', '')
        l[i] = l[i].replace('_center_', '')
        temp[0] = int(l[i])
    if "good road" in l[i+1]:
        temp[1] = 'good road'
    else:
        temp[1] = 'bad road'
    if "good road" in l[i+2]:
        temp[3] = 'good road'
    else:
        temp[3] = 'bad road'
    final.append(temp)
final.sort()
fp = open(path+'\\my_final.csv', 'w')
for i in final:
    temp = ",".join(i[1:])
    temp = str(i[0]) + "," + temp
    temp += '\n'
    fp.write(temp)
fp.close()
fp = open(path+'\\my_final.csv', 'r')
l = fp.readlines()
fp.close()
for i in range(0, len(l)):
    l[i] = l[i].replace('\n','')
final = []
for i in l:
    temp = [0, 0, 0, 0, 0]
    temp2 = i.split(',')
    temp[0] = int(temp2[0])
    if temp2[1] == 'bad road':
        temp[1] = 1
        temp[4] = -2
    if temp2[2] == 'bad road':
        temp[2] = 1
        temp[4] = 1
    if temp2[3] == 'bad road':
        temp[3] = 1
        temp[4] = 2
    if temp[1] + temp[2] + temp[3] > 1:
        temp[4] = 1
    final.append(temp)
final.sort()
fp = open(path+'\\my_final.csv', 'w')
fp.write("Frame No.,Left,Center,Right,Type\n")
for i in final:
    temp = str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "," + str(i[4])
    temp += '\n'
    fp.write(temp)
fp.close()

shutil.rmtree(path+"\\Final")
shutil.rmtree(path+"\\Final_With_Sides")


fp1 = open(path+"\Final.txt")
l1 = fp1.readlines()
l1 = [x for x in l1 if x != '\n']
fp1.close()
fp2 = open(path+"\my_final.csv")
l2 = fp2.readlines()
l2[0] = l2[0].replace('\n', ','+"Lat,Long\n")
for i in range(1, len(l1)+1):
    l2[i] = l2[i].replace('\n', ','+l1[i-1])

l2 = l2[:len(l1)+1]
fp2 = open(path+"\my_final.csv", 'w')
fp2.writelines(l2)
fp2.close()


sr = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Road Analyzer</title>
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #floating-panel {
        position: absolute;
        top: 10px;
        left: 25%;
        z-index: 5;
        background-color: #fff;
        padding: 5px;
        border: 1px solid #999;
        text-align: center;
        font-family: 'Roboto','sans-serif';
        line-height: 30px;
        padding-left: 10px;
      }
      #floating-panel {
        margin-left: -52px;
      }
    </style>
  </head>
  <body>
    <div id="floating-panel">
      <button id="drop" onclick="drop()">Drop Markers</button>
      <input onclick="clearMarkers();" type=button value="Rem Markers">
      <input onclick="addLine();" type=button value="Add line">
	  <input onclick="removeLine();" type=button value="Rem line">
      <input onclick="saddLine();" type=button value="Add Snapped line">
	  <input onclick="sremoveLine();" type=button value="Rem Snapped line">
      <input onclick="setseg();" type=button value="Add Seg">
	  <input onclick="resetseg();" type=button value="Rem Seg">
    </div>
    <div id="map"></div>
    <script>
		var unsnapped;
		var snapped;
		var temp2;
		var seg=[];
        var beaches ="""
sr2 = """;
		var markers = [];
		var map;


        function initMap() {
          map = new google.maps.Map(document.getElementById('map'), 
		  {
			  zoom: 18,
			  center: {lat: 22.553447, lng:  72.923796},
			  mapTypeId: 'terrain'
          });
		  var symbolOne = {
          path: 'M -2,0 0,-2 2,0 0,2 z',
          strokeColor: '#F00',
          fillColor: '#F00',
          fillOpacity: 1
        };
        var symbolThree = {
          path: 'M -2,-2 2,2 M 2,-2 -2,2',
          strokeColor: '#292',
          strokeWeight: 4
        };
		var raw=[];
		for (var i=0; i<beaches.length;i++)
		{
			var latlng=new google.maps.LatLng(beaches[i][1],beaches[i][2]);
			raw.push(latlng);
		}
		var url=[];
		for (var i = 0; i < beaches.length; i++){
		url.push((beaches[i][1]).toString()+','+(beaches[i][2]).toString());}
		var url='https://roads.googleapis.com/v1/snapToRoads?path='+url.join('|')+'&interpolate=true&key=AIzaSyDxddnpyWGvoQUMbfs_QORQiVmDJgWP938';
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange = function() {
		  if (this.readyState == 4 && this.status == 200) {
			var myArr = JSON.parse(this.responseText);
			myfunc(myArr);
		  }
		};
		xmlhttp.open("GET", url, false);
		xmlhttp.send(null);
		function myfunc(myArr){
		snappedCoordinates = [];
		temp2=[];
		  for (var i = 0; i < myArr.snappedPoints.length; i++) {
			var latlng = new google.maps.LatLng(
				myArr.snappedPoints[i].location.latitude,
				myArr.snappedPoints[i].location.longitude);
			snappedCoordinates.push(latlng);
			temp2.push(latlng);
		  }
		for (var i=0; temp2.length>0; i+=2)
		{

			var temp=temp2.splice(0,2);
			 seg.push(new google.maps.Polyline({
			  path: temp,
			  geodesic: true,
			  strokeColor: 'red',
			  strokeOpacity: 1.0,
			  strokeWeight: 5,
			  zIndex: 1

        }));
		}
		console.log(snappedCoordinates)
		snapped = new google.maps.Polyline({
          path: snappedCoordinates,
		  icons: [
            {
              icon: symbolOne,
              offset: '0%'
            }, {
              icon: symbolThree,
              offset: '100%'
            }
          ],
          geodesic: true,
          strokeColor: '#00FF00',
          strokeOpacity: 1.0,
          strokeWeight: 5,
			  zIndex: 0

        });

		unsnapped = new google.maps.Polyline({
          path: raw,
		  icons: [
            {
              icon: symbolOne,
              offset: '0%'
            }, {
              icon: symbolThree,
              offset: '100%'
            }
          ],
          geodesic: true,
          strokeColor: '#FF0000',
          strokeOpacity: 1.0,
          strokeWeight: 2
        });
		}



      }

      function drop() {
        clearMarkers();
        for (var i = 0; i < beaches.length; i++) {
		if(beaches[i][0]!=0){
          addMarkerWithTimeout(beaches[i], i * 100);}
        }
      }

      function addMarkerWithTimeout(beach, timeout) {

	  var x;
	  var y;
	  if(beach[0]==1){x='C';y='red';}else if(beach[0]==2){x='R';y='yellow';}else if(beach[0]==-2){x='L';y='green';}
        var icon = {
	  path: google.maps.SymbolPath.CIRCLE,
    fillColor: y,
    fillOpacity: .8,
    anchor: new google.maps.Point(0,0),
    strokeWeight: 0,
    scale: 7}
		window.setTimeout(function() {
          markers.push(new google.maps.Marker({
            position:{lat: beach[1], lng: beach[2]},
            map: map,
			icon: icon,
			label:x,
            animation: google.maps.Animation.DROP
          }));
        }, timeout);
      }
	   function addLine() {
        unsnapped.setMap(map);
      }

      function removeLine() {
        unsnapped.setMap(null);
      }
	  function saddLine() {
		snapped.setMap(map);
      }

      function sremoveLine() {
		snapped.setMap(null);
      }
	  function setseg()
	  {
	  for(var i=0; i<seg.length; i++)
		{
			seg[i].setMap(map);
		}
	  }
	  function resetseg()
	  {
	  for(var i=0; i<seg.length; i++)
		{
			seg[i].setMap(null);
		}
	  }
      function clearMarkers() {
        for (var i = 0; i < markers.length; i++) {
          markers[i].setMap(null);
        }
        markers = [];
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDxddnpyWGvoQUMbfs_QORQiVmDJgWP938&callback=initMap">
    </script>
  </body>
</html>"""
temp_count = 0
with open(path +"\\my_final.csv") as f:
    first_line = f.readline()
    with open("out.csv", "w") as f1:
        for line in f:
            f1.write(line)
with open('out.csv', 'rt')as f:
    data = csv.reader(f, quoting=csv.QUOTE_NONE)
    arr = []
    for row in data:
        arr.append([float(row[-3]), float(row[-2]), float(row[-1])])
with open(path + '\\index.html', 'w') as t:
    t.write(sr + str(arr) + sr2)
os.remove('out.csv')
webbrowser.open(path+"\\index.html")
