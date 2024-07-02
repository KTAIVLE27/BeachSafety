# from django.shortcuts import render
# from django.contrib.auth.models import User
# from main.models import User  # Ensure this is the correct import
from django.shortcuts import render, redirect
from django.urls import reverse
from main.models import User

def admin_home(request):
    return render(request, 'adminpanel/admin_home.html')

def senario(request):
    return render(request, 'adminpanel/senario.html')

def board_manage(request):
    return render(request, 'adminpanel/board_manage.html')

def user_list_view(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'adminpanel/user_list.html', context)
  
def notice_manage(request):
    return render(request, 'adminpanel/notice_manage.html')

