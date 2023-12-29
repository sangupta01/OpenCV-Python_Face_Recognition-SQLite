# OpenCV program to detect face in real time
# import libraries of python OpenCV 
# where its functionality resides
import cv2 
import sqlite3
import numpy as np
 
# load the required trained XML classifiers
# https://github.com/Itseez/opencv/blob/master/
# data/haarcascades/haarcascade_frontalface_default.xml
# Trained XML classifiers describes some features of some
# object we want to detect a cascade function is trained
# from a lot of positive(faces) and negative(non-faces)
# images.
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# capture frames from a camera
cap = cv2.VideoCapture(0)

def sqlInsertEntry(userid, name):
    conn=sqlite3.connect("FaceDB.db")
    cmd="CREATE TABLE IF NOT EXISTS People (userid INT PRIMARY KEY NOT NULL, name STRING NOT NULL)"
    cursor=conn.execute(cmd)

    cmd="SELECT * FROM People WHERE userid="+str(userid)
    cursor=conn.execute(cmd)

    recordExists=0
    for row in cursor:
        recordExists=1
    if(recordExists==1):
        cmd="UPDATE People SET name="+name+" WHERE userid="+str(userid)
    else:
        cmd="INSERT INTO People(userid,name) Values("+str(userid)+","+name+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()

userid = input('enter user-id: ')
name = input('enter name (within ""): ')

sqlInsertEntry(userid, name)

sampleNum = 0
 
# loop runs if capturing has been initialized.
while 1: 
 
    # reads frames from a camera
    ret, img = cap.read() 
 
    # convert to gray scale of each frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    # Detects faces of different sizes in the input image
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
 
    for (x,y,w,h) in faces:
        sampleNum = sampleNum+1
        cv2.imwrite("dataSet/User."+str(userid)+"."+str(sampleNum)+".jpg",
                    gray[y:y+h, x:x+w])

        # To draw a rectangle in a face 
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) 

        # wait for 10 ms
        cv2.waitKey(10)

    cv2.imshow('img',img)
 
    cv2.waitKey(1)
    print(f"sampleNum:{sampleNum}")
    if (sampleNum > 100):
        break
 
# Close the window
cap.release()
 
# De-allocate any associated memory usage
cv2.destroyAllWindows()
