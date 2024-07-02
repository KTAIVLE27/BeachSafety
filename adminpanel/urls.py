from django.urls import path
from . import views

app_name = 'adminpanel'  # Define the app name for namespacing

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path('board_manage/', views.board_manage, name='board_manage'),
    path('senario/', views.senario, name='senario'),
    path('user_list/', views.user_list_view, name='user_list_view'),
    path('notice_manage/', views.notice_manage, name='notice_manage'),
]
