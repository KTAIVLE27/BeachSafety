from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.signin,name='signin'),
    path('logout/',  auth_views.LogoutView.as_view(), name='logout'),
    path("home", views.home,name='home'),
    path("myprofile", views.myprofile,name='myprofile'),
    path("board", views.board,name='board'),
    path("free_board", views.free_board,name='free_board'),
    path("chat", views.chat,name='chat'),
    path("cctv", views.cctv,name='cctv'),
    path("weather", views.control_view, name='weather'),
    path("signup", views.signup,name='signup'),
    path("risk", views.risk,name='risk'),
    path('adminpanel/', views.admin_panel, name='admin_panel'),
    path('admin/', admin.site.urls),
    path('adminpanel/', include('adminpanel.urls'))
]
