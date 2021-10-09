import cv2,os
import numpy as np
from django.conf import settings
import face_recognition


#This module captures images via webcam and performs face recognition

# path = 'media/people'
# images = []
# className = []
# myImagesList = os.listdir(path)
# print(myImagesList)


# for anImage in myImagesList:
#     currentImg = cv2.imread(f'{path}/{anImage}')
#     images.append(currentImg)
#     className.append(os.path.splitext(anImage)[0])

# print(className)


def findImageEncodings(images):
    encodingList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodingList.append(encode)
    return encodingList

# encodeListKnown = findImageEncodings(images)
# print('Encoding Complete')

class RecognVideoCamera(object):
	#
    def __init__(self):
        # path ='media/people'
        # images = []
        # className = []
        # myImagesList = os.listdir(path)
        # print(myImagesList)
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_image(self):
        path ='media/people'
        images = []
        className = []
        myImagesList = os.listdir(path)
        print(myImagesList)

        for anImage in myImagesList:
            currentImg = cv2.imread(f'{path}/{anImage}')
            images.append(currentImg)
            className.append(os.path.splitext(anImage)[0])
        
        print(className)

        encodeListKnown = findImageEncodings(images)
        print('Encoding Complete')

        success, img = self.video.read()
        print(success, img)

        smallImg = cv2.resize(img, (0,0),None,0.25,0.25)
        smallImg = cv2.cvtColor(smallImg, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(smallImg)
        encodesCurrentFrame = face_recognition.face_encodings(smallImg, facesCurrentFrame)

        for encodeFace, faceLocation in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown,encodeFace)

            print(faceDistance)

            matchIndex = np.argmin(faceDistance)
            count = 0

            if matches[matchIndex]:
                name = className[matchIndex].upper()
                print(name)
                y1,x2,y2,x1 = faceLocation
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                # cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2) 
                # cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                cv2.imwrite(f"media/recognize/{name}{count}.jpg", img)
                count += 1
            
            else:
                name = "Unknown"
                print(name)
                y1,x2,y2,x1 = faceLocation
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                # cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                # cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        #
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

