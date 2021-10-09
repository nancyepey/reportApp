from django.shortcuts import render,redirect

#
import cv2, os
from django.http.response import StreamingHttpResponse
from django.http import HttpResponse,JsonResponse
from skinRecog.camera import SkinVideoCamera
from PIL import Image
from django.contrib.auth.models import User
import face_recognition
import PIL.Image
import PIL.ImageDraw
from django.contrib import messages
from .forms import usernameForm
from face_recognition.face_recognition_cli import image_files_in_folder


# Create your views here.

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



def skin_video_feed(request):
	return StreamingHttpResponse(gen(SkinVideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def skindetect(request):
    return render(request,'skinRecog/skinDetect.html')


def resultskindetect(request):
    return render(request,'skinRecog/detecResults.html')


def skinn(request):
    return render(request,'skinRecog/skin.html')

def skinRGB(request):
	#
	rgbs = []
	img = Image.open("static/skin/m1.jpg")
	width_image=30 #width
	height_image=28 #height

	for y in range(height_image):
		#
		#height y axis vertical
		for x in range(width_image):
			#
			#horizontal
			r,g,b=img.getpixel((x,y))
			print("rgb for x:",x ,"y:", y, "=", "red : ",r,"green : ",g,"blue : ",b)
			if r > 132:
				rgbs.append((r,g,b))
			# rgbs.append((r,g,b))
			# context = {
			# 	'rgb': (r,g,b)
			# }
			# return render(request,'skinRecog/skin.html',context)

	print("end")
	context = {
		'rgbs' : rgbs
	}

	return render(request,'skinRecog/skin.html',context)



def skinColor(request):
	#pass
	if request.method == 'POST':
		username = request.POST['username']
		userIsThere = username_present(username)
		if userIsThere:
			print("User ",username, " exist!")
			# detect and crop forehead
			create_dataset_crop_pic(username)
		else:
			print("User Not Found")
    
	else:
		pass
	
	return render(request, 'skinRecog/skinColor.html')
    


def username_present(username):
	if User.objects.filter(username=username).exists():
		return True
	
	return False


def take_two_pic(directory):
	cap = cv2.VideoCapture(0)
	i = 0
	while(1):
		ret ,frame = cap.read()
		k=cv2.waitKey(1)
		if i==2:
			print('Done taking two pics')
			break
		if k==27:
			break
		elif k==ord('s'):
			cv2.imwrite(directory,'/'+str(i)+'.jpg', frame)
			i+=1
		cv2.imshow("capture", frame)
		
	#
	cap.release()
	cv2.destroyAllWindows()

def add_photos(request):
	if request.method=='POST':
		form=usernameForm(request.POST)
		data = request.POST.copy()
		username=data.get('username')
		if username_present(username):
			result = create_dataset_crop_pic(username)
			messages.success(request, f'Photos Taken, Croped, RGB Calculated')
			context = {
				'results' : result
			}
			print(context['results'])
			#return redirect('add-photos')
			return render(request,'skinRecog/add_pic.html', context)
		else:
			messages.warning(request, f'No such username found.')
			return redirect('add-photos')


	else:
		

		form=usernameForm()
		return render(request,'skinRecog/add_pic.html', {'form' : form})


def get_forehead(directory, username):
	count=0
	rgb_color = []
	for person_name in os.listdir(directory):
		if username==person_name:
			curr_directory = os.path.join(directory, person_name)
		#
		if not os.path.isdir(curr_directory):
			continue
		for imageFile in image_files_in_folder(curr_directory):
			count+=1
	
	X=[]
	y=[]
	i=0

	for person_name in os.listdir(directory):
		if username==person_name:
			curr_directory = os.path.join(directory, person_name)
		#
		if not os.path.isdir(curr_directory):
			continue
		for imageFile in image_files_in_folder(curr_directory):
			print(str(imageFile))
			# reading the mage
			image=cv2.imread(imageFile)
			unknown_image = face_recognition.load_image_file(image)
			face_locations = face_recognition.face_locations(unknown_image) # detects all the faces in image
			t = len(face_locations)
			print(len(face_locations))
			print(face_locations)
			face_landmarks_list = face_recognition.face_landmarks(unknown_image)
			# Drawing rectangles over the faces
			pil_image = PIL.Image.fromarray(unknown_image)
			for face_location in face_locations:
				#print(face_location)
				top,right,bottom,left =face_location
				draw_shape = PIL.ImageDraw.Draw(pil_image)
				im = PIL.Image.open(image)
				k = face_landmarks_list[0]['right_eyebrow']
				lbottom = face_landmarks_list[0]['right_eyebrow'][0][1]
				for k1 in k :
					if(lbottom>k1[1]):
						lbottom=k1[1]
				bottom=min(bottom,lbottom)
				print(bottom)
				im = im.crop((left, top, right, bottom))
				# create a directory to save the forehead
				if(os.path.exists('media/skin/forehead/{}/'.format(username))==False):
					os.makedirs('media/skin/forehead/{}/'.format(username))
				foreheadDirectory = 'media/skin/forehead/{}/'.format(id)

				#im.save("m1.jpg")
				im.save(foreheadDirectory+'/'+username+''+str(i)+'.jpg')
				contxt = get_RGB_pixel(foreheadDirectory+'/'+username+''+str(i)+'.jpg')
				rgb_color.append(contxt)
				i+=1
				draw_shape.rectangle([left, top, right, bottom],outline="blue")

	return rgb_color


# get RGB of each pixel
def get_RGB_pixel(image):
	#pass
	rgbs = []
	#get img
	img = Image.open(image)
	width_image=30 #width
	height_image=28 #height

	for y in range(height_image):
		#
		#height y axis vertical
		for x in range(width_image):
			#
			#horizontal
			r,g,b=img.getpixel((x,y))
			print("rgb for x:",x ,"y:", y, "=", "red : ",r,"green : ",g,"blue : ",b)
			if r > 132:
				rgbs.append((r,g,b))
			# rgbs.append((r,g,b))
			# context = {
			# 	'rgb': (r,g,b)
			# }
			# return render(request,'skinRecog/skin.html',context)

	print("end")
	context = {
		'rgbs' : rgbs
	}

	return context
	


def create_dataset_crop_pic(username):
	id = username
	if(os.path.exists('media/skin/{}/'.format(id))==False):
		os.makedirs('media/skin/{}/'.format(id))
	directory='media/skin/{}/'.format(id)

	# Detecting the face
	# Cropping the face
	print("Detecting and Cropping Face")
	#
	take_two_pic(directory)
	# crop the pics to get the forehead
	rgbs = get_forehead(directory, username)
	#display the image and RBG of each pixel in an image

	context = {
		'rgbs' : rgbs,
	}
	
	return context
