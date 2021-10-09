from django.urls import path
from . import views

urlpatterns = [
    path('skindetection/',views.skindetect,name='skindetect'),
    path('resultskindetect/',views.resultskindetect,name='resultskin_d'), 
    path('skin_video_feed',views.skin_video_feed,name='skin_video_feed'), 
    path('skinn',views.skinn,name='skinn'),
    path('skinRGB',views.skinRGB,name='skinRGB'),
    path('skinColor',views.skinColor,name='skinColor'),
    path('add_photos/', views.add_photos, name='add-photos'),
]