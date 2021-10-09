from django.urls import path
from . import views

urlpatterns = [
    path('dlibrec',views.index,name='dlibrec'),
    path('recFaceResult',views.recognFaceResult,name='recogresults'),
    path('recgn_video_feed', views.Recgnvideo_feed, name='recgn_video_feed'),
  
  

]


