from . import views
from django.urls import path

app_name = 'control'
urlpatterns = [
    path("", views.control_view,name='control'),
]

