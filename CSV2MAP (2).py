import csv
import webbrowser
sr="""<!DOCTYPE html>
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
sr2=""";
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
		var url='https://roads.googleapis.com/v1/snapToRoads?path='+url.join('|')+'&interpolate=true&key=<API KEY>';
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
    src="https://maps.googleapis.com/maps/api/js?key=<API KEY>=initMap">
    </script>
  </body>
</html>"""
with open('gps.csv','rt')as f:
    data = csv.reader(f,quoting=csv.QUOTE_NONE)
    arr=[]
    for row in data:
        arr.append([float(row[-3]),float(row[-2]),float(row[-1])])
with open('index.html','w') as t:
    t.write(sr+str(arr)+sr2)
webbrowser.open("index.html")
