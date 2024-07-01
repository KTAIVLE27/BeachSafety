from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.signin,name='signin'),
    path("index", views.index,name='index'),
    path("elements", views.elements,name='elements'),
    path("generic", views.generic,name='generic'),
    path("home", views.home,name='home'),
    path("myprofile", views.myprofile,name='myprofile'),
    path("board", views.board,name='board'),
    path("chat", views.chat,name='chat'),
    path("cctv", views.cctv,name='cctv'),
    path("weather", views.weather,name='weather'),
    path("signup", views.signup,name='signup'),
    path("risk", views.risk,name='risk'),
    path('adminpanel/', views.admin_panel, name='admin_panel'),
]
