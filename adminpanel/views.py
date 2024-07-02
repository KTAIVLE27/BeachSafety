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

from main.models import User
def user_list_view(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'adminpanel/user_list.html', context)