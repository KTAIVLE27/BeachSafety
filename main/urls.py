from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.signin, name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("home", views.home, name='home'),
    path("myprofile", views.myprofile, name='myprofile'),
    path("board", views.board, name='board'),
    path("free_board", views.free_board, name='free_board'),
    # path("chat", views.chat, name='chat'),
    path("cctv", views.cctv, name='cctv'),
    path("weather", views.control_view, name='weather'),
    path("signup", views.signup,name='signup'),
    path("risk", views.risk,name='risk'),
    path('forgotpw/', views.forgotpw, name='forgotpw'),
    path('adminpanel/', views.admin_panel, name='admin_panel'),
    path('create_freeboard/', views.create_freeboard, name='create_freeboard'),  
    path('myposts/', views.myposts, name='myposts'),
    path('agreement/', views.agreement, name='agreement'),
    path('board/<int:pk>/', views.board_detail, name='board_detail'),
    path('create_freeboard/', views.create_freeboard, name='create_freeboard'),
    path('free_board/<int:pk>/', views.freeboard_detail, name='freeboard_detail'),
    path('freeboard/edit/<int:pk>/', views.edit_freeboard, name='edit_freeboard'),
    path('delete/<int:post_id>/', views.delete_freeboard, name='delete_freeboard'),
    path('team_info', views.team_info, name='team_info'),
    path('load_prediction/', views.load_prediction, name='load_prediction'),
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),
    path('copyright', views.copyright, name='copyright'),
    # path("chat_message/", views.chat_message, name='chat_message'),
    path("chat/", views.chat, name='chat'),
    path("chat/clear_logs/", views.chat_clear_logs, name='chat_clear_logs'),
    path('auto-admin-login', views.auto_admin_login, name='auto-admin-login'),
]

