from django.shortcuts import render
from .faceRecognition import *

# Create your views here.
def index(request):
    return render(request,'lbphf/index.html')


# training_completed = ""
# train model using dataset
def train_model(request, training_completed):
	# training_completed = ""
	#training
	#label for training data
	faces,faceID = labels_for_training_data('media/trainingImages')
	#passing this into our train classifier to get our face recognizer
	face_recognizer = train_classifier(faces, faceID)
	#save the trainer, so we won't need to train it over and over
	face_recognizer.save('trainingData.yml')

	if face_recognizer:
		training_completed = "Training DONE"

	# context = {
	# 	'status' : training_completed
	# }

	# return render(request,'recognition/index.html', context)

	if face_recognizer:
		training_completed = "Training DONE"
		return True
	else:
		return False

def video_tester(Kname,confi):
	#This module captures images via webcam and performs face recognition
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()
	face_recognizer.read('trainingData.yml')#Load saved training data

	name = {0 : "Nancy",1 : "Marie", 2 : "Epey Nancy"}


	cap=cv2.VideoCapture(0)

	while True:
	    ret,test_img=cap.read()# captures frame and returns boolean value and captured image
	    faces_detected,gray_img=faceDetection(test_img)



	    for (x,y,w,h) in faces_detected:
	      cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=7)

	    # resized_img = cv2.resize(test_img, (1000, 700))
	    # cv2.imshow('face detection Tutorial ',resized_img)
	    # cv2.waitKey(10)


	    for face in faces_detected:
	        (x,y,w,h)=face
	        roi_gray=gray_img[y:y+w, x:x+h]
	        label,confidence=face_recognizer.predict(roi_gray)#predicting the label of given image
	        print("confidence:",confidence)
	        print("label:",label)
	        Kname=label
	        confi=confidence
	        draw_rect(test_img,face)
	        predicted_name=name[label]
	        if confidence < 47:#If confidence less than 47 then don't print predicted face text on screen
	           put_text(test_img,predicted_name,x,y)
	           break
	           cap.release()
	           cv2.destroyAllWindows


	    # resized_img = cv2.resize(test_img, (1000, 700))
	    resized_img = cv2.resize(test_img, (400, 400))
	    cv2.imshow('face recognition ',resized_img)
	    # cv2.waitKey(10)
	    if cv2.waitKey(10) == ord('q'):#wait until 'q' key is pressed
	        break


	cap.release()
	cv2.destroyAllWindows

	# return {Kname, confi}









