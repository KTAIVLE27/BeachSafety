from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.signin,name='signin'),
    path('logout/',  auth_views.LogoutView.as_view(), name='logout'),
    path("index", views.index,name='index'),
    path("elements", views.elements,name='elements'),
    path("generic", views.generic,name='generic'),
    path("home", views.home,name='home'),
    path("myprofile", views.myprofile,name='myprofile'),
    path("board", views.board,name='board'),
    path("free_board", views.free_board,name='free_board'),
    path("chat", views.chat,name='chat'),
    path("cctv", views.cctv,name='cctv'),
    # path("weather", views.weather,name='weather'),
    path("weather", views.control_view, name='weather'),
    path("signup", views.signup,name='signup'),
    path("risk", views.risk,name='risk'),
    path('adminpanel/', views.admin_panel, name='admin_panel'),
    
]
