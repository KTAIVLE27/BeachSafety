from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import logging
from django.http import HttpResponseForbidden
from .models import *
from .forms import SignUpForm, PostForm, PasswordResetForm
from .utils import get_weather_item

def is_admin(user):
    return user.is_authenticated and user.user_id == 'admin' and user.user_name == 'admin' and user.check_password('aivle2024!')

def forgotpw(request):
    return render(request, 'forgotpw.html')

#@login_required
#@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'adminpanel/admin_home.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def myprofile(request):
    if request.method == 'POST':
        user = request.user

        user_email = request.POST.get('user_email')
        user_phone = request.POST.get('user_phone')
        user_address = request.POST.get('user_address')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # 비밀번호 확인 및 설정
        if password1 and password2:
            if password1 == password2:
                if user.check_password(password1):
                    messages.error(request, '새 비밀번호는 현재 비밀번호와 다르게 설정해 주세요.')
                    return redirect('myprofile')
                else:
                    user.set_password(password1)
                    password_changed = True
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
                return redirect('myprofile')
        else:
            password_changed = False

        # 이메일 변경
        if user_email and user_email != user.user_email:
            user.user_email = user_email

        # 휴대폰 번호 변경
        if user_phone and user_phone != user.user_phone:
            user.user_phone = user_phone

        # 주소 변경
        if user_address and user_address != user.user_address:
            user.user_address = user_address

        user.save()
        messages.success(request, '프로필 정보가 성공적으로 변경되었습니다.')
        return redirect('myprofile')
    else:
        return render(request, 'myprofile.html')

@login_required
def board(request):
    return render(request, 'board.html')

@login_required
def free_board(request):
    return render(request, 'free_board.html')

@login_required
def chat(request):
    return render(request, 'chat.html')

@login_required
def cctv(request):
    beaches = Beach.objects.all()
    cctvs = CCTV.objects.select_related('beach_no')
    context = {
        'beaches': beaches,
        'cctvs': cctvs,
    }
    return render(request, 'cctv.html', context)

@login_required
def risk(request):
    return render(request, 'risk.html')

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '게시물이 성공적으로 작성되었습니다.')
            return redirect('board')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form})

def signin(request):
    user = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=user_id, password=password)
            if user is not None:
                login(request, user)
                if user.user_role == 'supervisor':
                    return redirect('supervisor_dashboard')
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
    return render(request, 'signin.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.user_role = 'police'
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # 유효성 검사 오류가 발생하면 다시 회원가입 페이지를 렌더링합니다.
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def control_view(request):
    forecast_data_items = get_weather_item()
    forecast_data = dict(forecast_data_items)

    weather_data = {
        'weather_of_today': forecast_data.get('TMP', 'N/A'),
        'highest_temp_of_today': forecast_data.get('TMX', 'N/A'),
        'lowest_temp_of_today': forecast_data.get('TMN', 'N/A'),
        'temperature': forecast_data.get('TMP', 'N/A'),
        'rainfall': forecast_data.get('PCP', 'N/A'),
        'wind_ew': forecast_data.get('UUU', 'N/A'),
        'wind_ns': forecast_data.get('VVV', 'N/A'),
        'humidity': forecast_data.get('REH', 'N/A'),
        'precipitation': forecast_data.get('PTY', 'N/A'),
        'wind_direction': forecast_data.get('VEC', 'N/A'),
        'wind_speed': forecast_data.get('WSD', 'N/A'),
    }

    context = {
        'weather_data': weather_data
    }
    return render(request, 'weather.html', context)


def forgotpw(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('user_id')
            user_name = form.cleaned_data.get('user_name')
            user_phone = form.cleaned_data.get('user_phone')
            new_password1 = form.cleaned_data.get('new_password1')

            try:
                user = User.objects.get(user_id=user_id, user_name=user_name, user_phone=user_phone)
                user.set_password(new_password1)
                user.save()
                messages.success(request, 'Password has been reset successfully.')
                return redirect('signin')
            except User.DoesNotExist:
                messages.error(request, 'User with provided details does not exist.')
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = PasswordResetForm()
    return render(request, 'forgotpw.html', {'form': form})


def myposts(request):
    # 내가 쓴 글을 가져오는 로직을 추가하세요.
    return render(request, 'myposts.html')

def agreement(request):
    # 내가 쓴 글을 가져오는 로직을 추가하세요.
    return render(request, 'agreement.html')

