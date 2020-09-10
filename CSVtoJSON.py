import csv
with open('gps.csv','rt')as f:
    data = csv.reader(f,quoting=csv.QUOTE_NONE)
    arr=[]
    for row in data:
        arr.append([float(row[-3]),float(row[-2]),float(row[-1])])
with open('gps.txt','w') as t:
    t.write(str(arr))
