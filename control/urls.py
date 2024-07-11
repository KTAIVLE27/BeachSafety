from . import views
from django.urls import path
from .views import send_sms

app_name = 'control'
urlpatterns = [
    path("", views.control_view,name='control'),
    path('send-sms/', send_sms, name='send_sms'),
    path('video_feed/<int:cctv_code>/', views.video_feed, name='video_feed'),
]

