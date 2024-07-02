from . import views
from django.urls import path

urlpatterns = [
    path("", views.control_view,name='control'),
]

