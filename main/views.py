from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import logging
from django.http import HttpResponseForbidden

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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if is_admin(user):
                return redirect('admin_panel') 
            return redirect('/')  # 'home'은 home 페이지의 URL 패턴 이름이라고 가정
        else:
            messages.error(request, '이메일 또는 비밀번호가 잘못되었습니다.')
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 이 부분에서 password1과 password2를 사용해야 합니다.
            password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


