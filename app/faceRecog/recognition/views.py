import cv2
from django.shortcuts import render


from django.http.response import StreamingHttpResponse

#
# from .models import *
from django.http import HttpResponse,JsonResponse
from recognition.camera import VideoCamera, VideoToImage, VideoCameraRec

from lbphf.views import train_model, video_tester

# Create your views here.
def index(request):
    return render(request,'recognition/index.html')

def camera(request):
    return render(request,'recognition/camera.html')

def rec_camera(request):
    return render(request,'recognition/rec_camera.html')


def createimages(request):
	#
	return render(request,'recognition/createimages.html')

        
def video_to_image(request):
	cap=cv2.VideoCapture(0)

	count = 0
	while True:
	    ret,test_img=cap.read()
	    if not ret :
	        continue
	    cv2.imwrite("media/imagesCreated/nancy/frame%d.jpg" % count, test_img)     # save frame as JPG file
	    #cv2.imwrite("2/frame%d.jpg" % count, test_img) 
	    count += 1
	    resized_img = cv2.resize(test_img, (1000, 700))
	    cv2.imshow('capturing images ',resized_img)
	    if cv2.waitKey(10) == ord('q') or count == 101:#wait until 'q' key is pressed
	        break


	cap.release()
	cv2.destroyAllWindows
	count -= 1
	context = {
		'number' : count
	}

	return render(request,'recognition/createimages.html',context)

    

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def rec_video_feed(request):
	return StreamingHttpResponse(gen(VideoCameraRec()),
					content_type='multipart/x-mixed-replace; boundary=frame')

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

def video_to_image_feed(request):
	return StreamingHttpResponse(gen(VideoToImage()),
					content_type='multipart/x-mixed-replace; boundary=frame')

training_completed = ""
def go_train(request):
    train_model(request, training_completed)
    # if :
    # 	training_completed = "DONE"
    context = {
		'status' : training_completed
	}
    return render(request,'recognition/index.html', context)


name=""
confidence=""
def video_test(request):
	video_tester(name, confidence)
	context = {
		'name' : name,
		'confidence': confidence
	}
	return render(request,'recognition/index.html',context)

