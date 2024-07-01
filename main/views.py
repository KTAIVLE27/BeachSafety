from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import logging
from django.http import HttpResponseForbidden
from .forms import SignUpForm

def is_admin(user):
    return user.is_authenticated and user.username == 'aivle@kt.com' and user.check_password('aivle27')

@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'adminpanel/admin_home.html')

def index(request):
    return render(request, 'index.html')

def elements(request):
    return render(request, 'elements.html')

def generic(request):
    return render(request, 'generic.html')

@login_required
def home(request):
    return render(request, 'home.html')

def myprofile(request):
    return render(request, 'myprofile.html')

def board(request):
    return render(request, 'board.html')

def free_board(request):
    return render(request, 'free_board.html')

def chat(request):
    return render(request, 'chat.html')

def cctv(request):
    return render(request, 'cctv.html')

def weather(request):
    return render(request, 'weather.html')

def risk(request):
    return render(request, 'risk.html')

def signin(request):
    user = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = user_id, password = password)
            if user is not None:
                login(request, user)
                if user.user_role == 'supervisor':
                    return redirect('superviosr_dashbord')
                elif user.user_role == 'police':
                    return redirect('home')
                elif user.user_role == 'admin':
                    return redirect('admin_panel')    
            else:
                messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
        else:
                messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form' : form})




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.user_role = 'police'
            user.save()
            login(request, user) # 로그인 처리
            return redirect('home')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


