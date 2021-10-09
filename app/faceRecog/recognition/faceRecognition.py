import cv2
import os #os to create labels for our training data, for file related operations
import numpy as np #to data or labels to our classifier

def faceDetection(test_img):
	#converting image to gray; removing color
	gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
	#using haar classifier, contains features to detect faces
	face_haar_cascade=cv2.CascadeClassifier('D:/period/faceReg/neha01/mine/HaarCascade/haarcascade_frontalface_default.xml')
	#detectMultiScale will return the rectangle where the face is detected in the image(gray img)
	# scaleFactor is decreasing the size of the image by 32% blc images bigger in size will not work with the classifier so we try to decrease the size of the image so that the image have more chances in getting detected by the classifier
	# minNeighbors=5, means it will have at least 5 neighbors for it to be detected as a true position, if you reduces it you can have false positives
	faces = face_haar_cascade.detectMultiScale(gray_img, scaleFactor=1.32, minNeighbors=5)
	# returning faces (rectangle of the faces) and gray image (when training our classifier it will need this gray image)
	# when we call this fxn it will give us, rectangle of the faces, img n gray img
	return faces, gray_img

#to generate labels for each of the images in our training data
# the label should only be intergers
def labels_for_training_data(directory):
	#
	faces=[]
	faceID=[]


	#os.walk will go recursively into directories
	for path, subdirnames, filenames in os.walk(directory):
		#
		#
		for filename in filenames:
			if filename.startswith("."):
				print("Skipping system file")
				continue

			#if it not system file
			#fetched the id ie 0, 1 etc
			id = os.path.basename(path)
			print("id: ", id)
			img_path=os.path.join(path, filename)
			print("img_path: ", img_path)

			test_img=cv2.imread(img_path)
			#if image is not loaded properly
			if test_img is None:
				print("Image not loaded properly")
				continue

			#call face detection
			faces_rect,gray_img = faceDetection(test_img)
			

			#if our classifier have more than one face skip it so that we won't confuse it
			if len(faces_rect)!=1:
				continue #Since we are assuming only single person images are being fed to classifier
			#(x,y,w,h)=faces_rect[0] rectangle will be return by our faces_rect
			(x,y,w,h)=faces_rect[0]
			#we want to crop that from gray image (the face part) and feed (only the face part) it our classifier
			roi_gray=gray_img[y:y+w,x:x+h]#cropping region of interest i.e. face area from grayscale image
			#adding it to the face
			faces.append(roi_gray)
			#adding it to the id
			faceID.append(int(id))
			

	
	#return faces(part of the image (gray image) which is the face) and lable
	return faces,faceID        
    
    


# train our classifier on training images
# faces part of the image wc is the face of the gray image and face id
def train_classifier(faces,faceID):
	# the recognition techniques like facial faces, LBPH we are using LBPH
	#LBPH is local binary pattern histogram
    face_recognizer=cv2.face.LBPHFaceRecognizer_create()
    # load variable inside classifier to recognize our face
    # training it on the data we generated
    #this recognizers takes in the labels as a numpy array
    face_recognizer.train(faces,np.array(faceID))
    #return the recognizer
    return face_recognizer


#Below function draws bounding boxes around detected face in image
#this fxn takes the test image and rectangle coordinates of the face detected in image
def draw_rect(test_img,face):
	#getting the location
    (x,y,w,h)=face
    #creating a bounding bow
    cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=5)


#Below function writes name of person for detected label
#taking in the x y cordinates where we will put our text, the text we want to display and the image
def put_text(test_img,text,x,y):
	#FONT_HERSHEY_DUPLEX is the font, 2 font thickness and 4 size of the font
    cv2.putText(test_img,text,(x,y),cv2.FONT_HERSHEY_DUPLEX,2,(255,0,0),4)
    # cv2.putText(test_img,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    # cv2.putText(frame,'Hello World : After flip',(100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)


