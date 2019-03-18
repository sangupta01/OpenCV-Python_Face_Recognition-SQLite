import cv2,os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()

path='dataset'

def getImagesWithID(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #create empth face list
    faces=[]
    #create empty ID list
    IDs=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        faceImg=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        faceNp=np.array(faceImg,'uint8')
        #getting the Id from the image
        ID=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(faceNp)

        #If a face is there then append that in the list as well as Id of it
        IDs.append(ID)
        cv2.imshow("training",faceNp)
        cv2.waitKey(10)

    return np.array(IDs),faces,

Ids,faces = getImagesWithID('dataset')
recognizer.train(faces, Ids)
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()
