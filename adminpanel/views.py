from django.shortcuts import render
from django.contrib.auth.models import User


def admin_home(request):
    return render(request, 'adminpanel/admin_home.html')

def user_list(request):
    return render(request, 'adminpanel/user_list.html')

def senario(request):
    return render(request, 'adminpanel/senario.html')

def board_manage(request):
    return render(request, 'adminpanel/board_manage.html')

def notice_manage(request):
    return render(request, 'adminpanel/notice_manage.html')