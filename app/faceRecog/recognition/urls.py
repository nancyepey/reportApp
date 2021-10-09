from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index1'),
    path('camera',views.camera,name='camera'),
    path('rec_camera',views.rec_camera,name='rec_camera'),
    path('createimages',views.createimages,name='createimages'),
    # path('facecam_feed', views.facecam_feed, name='facecam_feed'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('rec_video_feed', views.rec_video_feed, name='rec_video_feed'),
    #path('stop_video_feed', views.stop_video_feed, name='stop_video_feed'),
    path('video_to_image', views.video_to_image, name='video_to_image'),
    path('train', views.go_train, name='train'),
    path('video_rec', views.video_test, name='video_rec'),
  
  

]