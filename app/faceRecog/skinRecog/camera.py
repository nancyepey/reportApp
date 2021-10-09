import cv2,os
import numpy as np
from django.conf import settings
import imutils
import numpy as np

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

class SkinVideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        grabbed, frame = self.video.read()
        print(grabbed, frame)

        #resized
        frame = imutils.resize(frame, width = 400)
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        skinMask = cv2.inRange(converted, lower, upper)

        #apply a series of erosions
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        skinMask = cv2.erode(skinMask, kernel, iterations = 2)
        skinMask = cv2.dilate(skinMask, kernel, iterations = 2)

        #blur the mask to help remove noise, then apply the mask
        #to the frame
        skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
        skin = cv2.bitwise_and(frame, frame, mask = skinMask)

        #show the skin in the image along with the mask
        frame_flip = cv2.flip(np.hstack([frame, skin]), 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        count = 0
        cv2.imwrite("media/imgsCreatedSkin/skinDetect%d.jpg" % count, frame_flip)
        return jpeg.tobytes()