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

# @login_required
# def myprofile(request):
#     return render(request, 'myprofile.html')

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

# myapp/views.py
# from django.shortcuts import render
# from .utils import fetch_data_from_kma
# import arrow

# STATUS_OF_SKY = {
#     "1": "맑음",
#     "3": "구름많음",
#     "4": "흐림"
# }

# STATUS_OF_PRECIPITATION = {
#     "0": "없음",
#     "1": "비",
#     "2": "비/눈",
#     "3": "눈",
#     "5": "빗방울",
#     "6": "빗방울눈날림",
#     "7": "눈날림"
# }

# def weather_view(request):
#     current_time_kst = arrow.now('Asia/Seoul')

#     sky = fetch_data_from_kma(current_time_kst, '3', 'SKY', '0500')
#     precipitation = fetch_data_from_kma(current_time_kst, '4', 'PTY', '0500')
#     lowest_temp_of_today = fetch_data_from_kma(current_time_kst, '5', 'TMN', '0600')
#     highest_temp_of_today = fetch_data_from_kma(current_time_kst, '16', 'TMX', '1500')
#     temperature = fetch_data_from_kma(current_time_kst, '1', 'T1H', '0500')
#     rainfall = fetch_data_from_kma(current_time_kst, '1', 'RN1', '0500')
#     wind_ew = fetch_data_from_kma(current_time_kst, '1', 'UUU', '0500')
#     wind_ns = fetch_data_from_kma(current_time_kst, '1', 'VVV', '0500')
#     humidity = fetch_data_from_kma(current_time_kst, '1', 'REH', '0500')
#     wind_direction = fetch_data_from_kma(current_time_kst, '1', 'VEC', '0500')
#     wind_speed = fetch_data_from_kma(current_time_kst, '1', 'WSD', '0500')

#     weather_data = {
#         "weather_of_today": STATUS_OF_SKY.get(sky, "Unknown"),
#         "precipitation": STATUS_OF_PRECIPITATION.get(precipitation, "Unknown"),
#         "lowest_temp_of_today": lowest_temp_of_today,
#         "highest_temp_of_today": highest_temp_of_today,
#         "temperature": temperature,
#         "rainfall": rainfall,
#         "wind_ew": wind_ew,
#         "wind_ns": wind_ns,
#         "humidity": humidity,
#         "wind_direction": wind_direction,
#         "wind_speed": wind_speed,
#     }

#     return render(request, 'weather.html', {'weather_data': weather_data})

from django.shortcuts import render
from .utils import fetch_data_from_kma
import arrow

STATUS_OF_SKY = {
    "1": "맑음",
    "3": "구름많음",
    "4": "흐림"
}

STATUS_OF_PRECIPITATION = {
    "0": "없음",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "5": "빗방울",
    "6": "빗방울눈날림",
    "7": "눈날림"
}

def weather_view(request):
    current_time_kst = arrow.now('Asia/Seoul')

    sky = fetch_data_from_kma(current_time_kst, '3', 'SKY', '0500')
    precipitation = fetch_data_from_kma(current_time_kst, '4', 'PTY', '0500')
    lowest_temp_of_today = fetch_data_from_kma(current_time_kst, '5', 'TMN', '0600')
    highest_temp_of_today = fetch_data_from_kma(current_time_kst, '16', 'TMX', '1500')
    temperature = fetch_data_from_kma(current_time_kst, '1', 'T1H', '0500')
    rainfall = fetch_data_from_kma(current_time_kst, '1', 'RN1', '0500')
    wind_ew = fetch_data_from_kma(current_time_kst, '1', 'UUU', '0500')
    wind_ns = fetch_data_from_kma(current_time_kst, '1', 'VVV', '0500')
    humidity = fetch_data_from_kma(current_time_kst, '1', 'REH', '0500')
    wind_direction = fetch_data_from_kma(current_time_kst, '1', 'VEC', '0500')
    wind_speed = fetch_data_from_kma(current_time_kst, '1', 'WSD', '0500')

    weather_data = {
        "weather_of_today": STATUS_OF_SKY.get(sky, "Unknown"),
        "precipitation": STATUS_OF_PRECIPITATION.get(precipitation, "Unknown"),
        "lowest_temp_of_today": lowest_temp_of_today,
        "highest_temp_of_today": highest_temp_of_today,
        "temperature": temperature,
        "rainfall": rainfall,
        "wind_ew": wind_ew,
        "wind_ns": wind_ns,
        "humidity": humidity,
        "wind_direction": wind_direction,
        "wind_speed": wind_speed,
    }

    return render(request, 'weather.html', {'weather_data': weather_data})


