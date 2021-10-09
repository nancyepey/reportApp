from django.shortcuts import render
#
import cv2
from django.http.response import StreamingHttpResponse
from face_recog_dlib.face_iden_rec import RecognVideoCamera
from django.http import HttpResponse,JsonResponse

# Create your views here.

def index(request):
    return render(request,'face_recog_dlib/home.html')


def recognFaceResult(request):
    return render(request,'face_recog_dlib/recognResult.html')



def gen(camera):
	while True:
		frame = camera.get_image()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def Recgnvideo_feed(request):
	return StreamingHttpResponse(gen(RecognVideoCamera()),
			    content_type='multipart/x-mixed-replace; boundary=frame')

