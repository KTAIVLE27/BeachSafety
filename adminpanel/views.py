from django.shortcuts import render
from django.contrib.auth.models import User


def admin_home(request):
    return render(request, 'adminpanel/admin_home.html')

def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'adminpanel/user_list.html', {'users': users})

def senario(request):
    return render(request, 'adminpanel/senario.html')

def board_manage(request):
    return render(request, 'adminpanel/board_manage.html')
