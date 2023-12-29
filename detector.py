import cv2 
import numpy as np
import sqlite3

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# capture frames from a camera
cap = cv2.VideoCapture(0)
 
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read('recognizer/trainingData.yml')

userid=0
font = cv2.FONT_HERSHEY_SIMPLEX

def walkDb():
    conn=sqlite3.connect("FaceDB.db")
    cmd="PRAGMA table_info(People)"
    cursor=conn.execute(cmd)
    print(cursor)

    cmd="SELECT * FROM People"
    cursor=conn.execute(cmd)
    for row in cursor:
        print("%s %s %s %s" % (row[0], row[1], row[2], row[3]))
    conn.close()

def getProfile(userid):
    conn=sqlite3.connect("FaceDB.db")
    cmd="SELECT * FROM People WHERE USERID="+str(userid)
    cursor=conn.execute(cmd)
    profile=None

    for row in cursor:
        profile=row
    conn.close()
    return profile

# loop runs if capturing has been initialized.
while 1: 
    #walkDb()

    # reads frames from a camera
    ret, img = cap.read() 
 
    # convert to gray scale of each frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    # Detects faces of different sizes in the input image
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
 
    for (x,y,w,h) in faces:
        # To draw a rectangle in a face 
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) 
        userid,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getProfile(userid)

        if(profile!=None):
            cv2.putText(img,str(profile[1]),(x,y-10),font,0.55,(0,255,0),1)

    cv2.imshow('img',img)
 
    # Wait for Esc key to stop
    if(cv2.waitKey(1) == ord('q')):
        break;
 
# Close the window
cap.release()
 
# De-allocate any associated memory usage
cv2.destroyAllWindows()
