import os


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


fp = open('D:\Test\Show2\my_final.csv', 'w')
fp.close()
dirName = 'D:\Test\Show2\Final_With_Sides'
listOfFiles = getListOfFiles(dirName)
for i in listOfFiles:
    os.system("python -W ignore scripts/label_image.py --graph=tf_files/retrained_graph.pb --image="+i)