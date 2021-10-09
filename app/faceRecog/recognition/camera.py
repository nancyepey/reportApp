import cv2,os,urllib.request
import numpy as np
from django.conf import settings

from lbphf.views import train_model, video_tester

import recognition.faceRecognition as fr


#This module captures images via webcam and performs face recognition
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('trainingData.yml')#Load saved training data

name = {0 : "Nancy", 1 : "Marie"}

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))



class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		print(success, image)
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		print(faces_detected)
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()



class VideoCameraRec(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		print(success, image)
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.

		image = cv2.flip(image,1)

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		print(faces_detected)
		count = 0
		for face in faces_detected:
			(x,y,w,h)=face
			roi_gray=gray[y:y+w, x:x+h]
			label,confidence=face_recognizer.predict(roi_gray)#predicting the label of given image
			print("confidence:",confidence)
			print("label:",label)
			# fr.draw_rect(image,face)
			# draw rect
			(x,y,w,h)=face
			cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),thickness=5)
			predicted_name=name[label]
			# cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
			# count = 0
			if confidence < 49:
				# fr.put_text(image,predicted_name,x,y)
				# write text on
				
				#text = "{}: {:.2f}%".format(predicted_name, confidence)
				text = f"{predicted_name}"
				cv2.putText(image,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),4)
				cv2.imwrite(f"media/peopleRecognized/{predicted_name}{count}.jpg", image)
				count += 1
			#If confidence less than 37 then don't print predicted face text on screen

		# frame_flip = cv2.flip(image,1)
		# if confidence < 49:
		# 	fr.put_text(image,predicted_name,x,y)
		# ret, jpeg = cv2.imencode('.jpg', frame_flip)
		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()



class VideoToImage(object):
	
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success,test_img = self.video.read()
		print(success,test_img)
		count = 0
		while True:
			if not success:
				continue
			cv2.imwrite("media/imagesCreated/frame%d.jpg" % count, test_img)     # save frame as JPG file
			count += 1
			resized_img = cv2.resize(test_img, (1000, 700))
			# cv2.imshow('face detection Tutorial ',resized_img)
			if count == 2:#wait until 'q' key is pressed
		 		break
			frame_flip = cv2.flip(resized_img,1)
			ret, jpeg = cv2.imencode('.jpg', frame_flip)
			return jpeg.tobytes()
	
	


	# cap.release()
	# cv2.destroyAllWindows