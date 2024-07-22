from django.urls import path
from . import views


app_name = 'adminpanel'  # Define the app name for namespacing

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path('board_manage/', views.board_manage, name='board_manage'),
    path('delete-boards/', views.delete_boards, name='delete_boards'),
    path('senario/', views.senario, name='senario'),
    path('csv_upload/', views.csv_upload, name='csv_upload'),
    path('delete-senario/', views.delete_senario, name='delete_senario'),
    path('user_list/', views.user_list_view, name='user_list_view'),
    path('user_list/<int:user_no>/', views.user_detail, name='user_detail'),
    path('delete_users/', views.delete_users, name='delete_users'),
    path('notice_manage/', views.notice_manage, name='notice_manage'),
    path('delete-notice-boards/', views.delete_notice_boards, name='delete_notice_boards'),
    path('create_notice/', views.create_notice, name='create_notice'),
    path('notice/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('notice/edit/<int:pk>/', views.edit_notice, name='edit_notice'),
    path('board/<int:pk>/', views.board_detail, name='board_detail'),
    path("control/", views.control_load,name='control'),
    path("home/", views.main_load,name='home'),
    path('notice/<int:pk>/download/', views.generate_presigned_url, name='generate_presigned_url'),


]
