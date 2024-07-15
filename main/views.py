from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging
from django.http import HttpResponseForbidden
from .models import *
from .forms import *
from .utils import get_weather_item
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
import json
from control.utils import *
from django.db.models import Q
import boto3
from django.conf import settings
import joblib

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
    home_notices = Notice_board.objects.all().order_by('-notice_id')[:5]  # 최신 순서로 상위 5개 공지사항
    home_event = Event_board.objects.all().order_by('-event_id')[:5]  # 최신 순서로 상위 5개 이벤트
    context = {
        'home_notices': home_notices,
        'home_event': home_event,
    }
    
    context_rip = {
        'GYEONGPO_score_msg': get_beach_score_msg('GYEONGPO'),
        'GORAEBUL_score_msg': get_beach_score_msg('GORAEBUL'),
        'NAKSAN_score_msg': get_beach_score_msg('NAKSAN'),
        'DAECHON_score_msg': get_beach_score_msg('DAECHON'),
        'MANGSANG_score_msg': get_beach_score_msg('MANGSANG'),
        'SOKCHO_score_msg': get_beach_score_msg('SOKCHO'),
        'SONGJUNG_score_msg': get_beach_score_msg('SONGJUNG'),
        'IMRANG_score_msg': get_beach_score_msg('IMRANG'),
        'JUNGMUN_score_msg': get_beach_score_msg('JUNGMUN'),
        'HAE_score_msg': get_beach_score_msg('HAE'),
        
        'GYEONGPO_lon': get_beach_lon('경포 해수욕장'),
        'GORAEBUL_lon': get_beach_lon('고래불 해수욕장'),
        'NAKSAN_lon': get_beach_lon('낙산 해수욕장'),
        'DAECHON_lon': get_beach_lon('대천 해수욕장'),
        'MANGSANG_lon': get_beach_lon('망상 해수욕장'),
        'SOKCHO_lon': get_beach_lon('속초 해수욕장'),
        'SONGJUNG_lon': get_beach_lon('송정 해수욕장'),
        'IMRANG_lon': get_beach_lon('임랑 해수욕장'),
        'JUNGMUN_lon': get_beach_lon('중문 해수욕장'),
        'HAE_lon': get_beach_lon('해운대 해수욕장'),
        
        'GYEONGPO_lat': get_beach_lat('경포 해수욕장'),
        'GORAEBUL_lat': get_beach_lat('고래불 해수욕장'),
        'NAKSAN_lat': get_beach_lat('낙산 해수욕장'),
        'DAECHON_lat': get_beach_lat('대천 해수욕장'),
        'MANGSANG_lat': get_beach_lat('망상 해수욕장'),
        'SOKCHO_lat': get_beach_lat('속초 해수욕장'),
        'SONGJUNG_lat': get_beach_lat('송정 해수욕장'),
        'IMRANG_lat': get_beach_lat('임랑 해수욕장'),
        'JUNGMUN_lat': get_beach_lat('중문 해수욕장'),
        'HAE_lat': get_beach_lat('해운대 해수욕장'),   
    }
    context_json = json.dumps(context_rip)  # JSON 형식의 문자열로 변환
    combined_context = {
        **context,
        'context_rip_json': context_json  # JSON 문자열을 포함
    }
    return render(request, 'home.html', combined_context)

@login_required
def myprofile(request):
    if request.method == 'POST':
        user = request.user

        user_email = request.POST.get('user_email')
        user_phone = request.POST.get('user_phone')
        user_address = request.POST.get('user_address')
        user_detail_address = request.POST.get('user_detail_address')
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
            
        # 상세 주소 변경
        if user_detail_address and user_detail_address != user.user_detail_address:
            user.user_detail_address = user_detail_address

        user.save()
        messages.success(request, '프로필 정보가 성공적으로 변경되었습니다.')
        return redirect('myprofile')
    else:
        return render(request, 'myprofile.html')

@login_required
def board(request):
    beach_no = request.GET.get('beach_no')
    
    if beach_no == 'common':
        posts = Notice_board.objects.filter(beach_no__isnull=True).order_by('-notice_wdate')
    elif beach_no:
        posts = Notice_board.objects.filter(beach_no=beach_no).order_by('-notice_wdate')
    else:
        posts = Notice_board.objects.all().order_by('-notice_wdate')
    # 검색 기능
    search_keyword = request.GET.get('q', '')
    search_type  = request.GET.get('type', '')    
    if search_keyword:
        if len(search_keyword) > 1:
            if search_type == 'all': # 전체
                posts = posts.filter(Q (notice_title__icontains=search_keyword) 
                                              | Q (notice_contents__icontains=search_keyword) 
                                              | Q (user_no__user_name__icontains=search_keyword) )
            elif search_type =='title':
                posts = posts.filter(notice_title__icontains=search_keyword)
                
            elif search_type == 'content' :
                posts = posts.filter(notice_contents__icontains=search_keyword)
                
            elif search_type == 'writer' :
                posts = posts.filter(user_no__user_name__icontains=search_keyword)
        else:
            messages.error(request, '검색어는 2글자 이상 입력해주세요!')    
    
    # 페이징 처리
    paginator = Paginator(posts, 10)  # 페이지당 10개의 게시물
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    beaches = Beach.objects.all()
    beaches = Beach.objects.all()
    
    
    return render(request, 'board.html', {'notices': posts, 'beaches': beaches, 'selected_beach_no': beach_no, 'page_obj': page_obj})

@login_required
def board_detail(request, pk):
    try:
        post = Notice_board.objects.get(pk=pk)
        post.notice_views += 1  # 조회수 증가 
        post.save()
    except Notice_board.DoesNotExist:
        messages.error(request, "해당 게시글을 찾을 수 없습니다.")
        return redirect('board')
    
    return render(request, 'board_detail.html', {'post': post})


@login_required
def free_board(request):
    beach_no = request.GET.get('beach_no')
    if beach_no == 'common':
        posts = Event_board.objects.filter(beach_no__isnull=True).order_by('-event_wdate')
    elif beach_no:
        posts = Event_board.objects.filter(beach_no=beach_no).order_by('-event_wdate')
    else:
        posts = Event_board.objects.all().order_by('-event_wdate')
        
    # 검색 기능
    search_keyword = request.GET.get('q', '')
    search_type  = request.GET.get('type', '')    
    if search_keyword:
        if len(search_keyword) > 1:
            if search_type == 'all': # 전체
                posts = posts.filter(Q (event_title__icontains=search_keyword) 
                                              | Q (event_contents__icontains=search_keyword) 
                                              | Q (user_no__user_name__icontains=search_keyword) )
            elif search_type =='title':
                posts = posts.filter(event_title__icontains=search_keyword)
                
            elif search_type == 'content' :
                posts = posts.filter(event_contents__icontains=search_keyword)
                
            elif search_type == 'writer' :
                posts = posts.filter(user_no__user_name__icontains=search_keyword)
        else:
            messages.error(request, '검색어는 2글자 이상 입력해주세요!')   
    
    # 페이징 처리
    paginator = Paginator(posts, 10)  # 페이지당 10개의 게시물
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    beaches = Beach.objects.all()
    return render(request, 'free_board.html', {'posts': posts, 'page_obj': page_obj, 'beaches':beaches})

# 자유게시판 조회
@login_required
def freeboard_detail(request, pk):
    try:
        post = Event_board.objects.get(pk=pk)
        post.event_views += 1  # 조회수 증가
        post.save()
    except Event_board.DoesNotExist:
        messages.error(request, "해당 게시글을 찾을 수 없습니다.")
        return redirect('free_board')
    beaches = Beach.objects.all()
    return render(request, 'freeboard_detail.html', {'post': post, 'beaches':beaches})

#자유게시판 생성
@login_required
def create_freeboard(request):
    if request.method == 'POST':
        form = FreePostForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user_no = request.user
            event.event_wdate = timezone.now()
            if not event.beach_no:
                event.beach_no = None
            
            # 파일 업로드 (client 방식)
            if 'event_img' in request.FILES:
                file = request.FILES['event_img']
                
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                
                s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
                s3_key = f'event/{file.name}'
                s3.upload_fileobj(file, s3_bucket, s3_key, ExtraArgs={'ContentType': file.content_type})
                
                file_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}'
                event.event_img = file_url           
            event.save()
            return redirect('free_board')
    else:
        form = FreePostForm()
        
    beaches = Beach.objects.all()
    return render(request, 'create_freeboard.html', {'beaches': beaches})

# 자유게시판 수정
@login_required
def edit_freeboard(request, pk):
    post = get_object_or_404(Event_board, pk=pk)

    if request.user != post.user_no:
        return JsonResponse({'success': False})

    if request.method == 'POST':
        form = FreePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            event = form.save(commit=False)
            if event.beach_no == '':
                event.beach_no = None
                
            if 'event_img' in request.FILES:
                file = request.FILES['event_img']
                
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                
                s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
                s3_key = f'event/{file.name}'
                s3.upload_fileobj(file, s3_bucket, s3_key, ExtraArgs={'ContentType': file.content_type})
                
                file_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}'
                event.event_img = file_url
            else :
                event.event_img = request.POST.get('existing_event_img')  # 기존 이미지 유지                                
            event.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})

#자유게시판 삭제
@require_POST
def delete_freeboard(request, post_id):
    post = get_object_or_404(Event_board, pk=post_id, user_no=request.user)
    post.delete()
    return JsonResponse({'success': True})


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

def get_risk_level(score):
    if score < 30:
        return '관심'
    elif 30 <= score < 55:
        return '주의'
    elif 55 <= score < 80:
        return '경계'
    else:
        return '위험'
    
    
import pandas as pd
from pathlib import Path
@login_required
def risk(request):
    beaches = Beach.objects.all()
    return render(request, 'risk.html', {'beaches': beaches})

def load_prediction(request):
    beach_name = request.GET.get('beach_name')
    beach = Beach.objects.get(beach_name = beach_name)
    beach_api_code = beach.beach_api_code
    
    base_path = Path(__file__).resolve().parent.parent / 'main' / 'models'
    model_path = base_path/f'{beach_api_code}.pkl'


    if model_path.exists():
        model, feature_names, label_encoders = joblib.load(model_path)
        result = get_predict_data(beach_api_code, label_encoders)
        if result == 'NaN':
            return JsonResponse({'prediction': 'Invalid data'})
        else:
            wave_period, air_temp, water_temp, wind_speed, score_msg, wave_height, wind_direct = result

            input_data = {
                'wave_period': [wave_period],
                'air_temp': [air_temp],
                'water_temp': [water_temp],
                'wind_speed': [wind_speed],
                'score_msg': [score_msg],
                'wave_height': [wave_height],
                'wind_direct': [wind_direct]
            }
            df = pd.DataFrame(input_data)
            df = df[feature_names]
            
            prediction = model.predict(df)
            score = prediction[0]
            risk_level = get_risk_level(score)
            return JsonResponse({'prediction': score, 'risk_level': risk_level})
    else:
        return JsonResponse({'prediction': 'Model not found', 'score': 'NaN', 'risk_level': '알 수 없음'})
        

def signin(request):
    # 사용자가 이미 로그인한 상태인지 확인
    if request.user.is_authenticated:
        if request.user.user_role == 'police':
            return redirect('home')
        elif request.user.user_role == 'admin':
            return redirect('adminpanel:admin_home')
        elif request.user.user_role == 'supervisor':
            return redirect('control:control')

    # POST 요청 처리
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=user_id, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') if user.user_role == 'police' else redirect('adminpanel:admin_home') if user.user_role == 'admin' else redirect('control:control')
            else:
                messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
        else:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
    else:
        form = AuthenticationForm()

    # 로그인 폼 렌더링
    return render(request, 'signin.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.user_role = 'police'
            user.save()
            return redirect('signin')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# def control_view(request):
#     forecast_data_items = get_weather_item()
#     forecast_data = dict(forecast_data_items)

#     weather_data = {
#         'weather_of_today': forecast_data.get('TMP', 'N/A'),
#         'highest_temp_of_today': forecast_data.get('TMX', 'N/A'),
#         'lowest_temp_of_today': forecast_data.get('TMN', 'N/A'),
#         'temperature': forecast_data.get('TMP', 'N/A'),
#         'rainfall': forecast_data.get('PCP', 'N/A'),
#         'wind_ew': forecast_data.get('UUU', 'N/A'),
#         'wind_ns': forecast_data.get('VVV', 'N/A'),
#         'humidity': forecast_data.get('REH', 'N/A'),
#         'precipitation': forecast_data.get('PTY', 'N/A'),
#         'wind_direction': forecast_data.get('VEC', 'N/A'),
#         'wind_speed': forecast_data.get('WSD', 'N/A'),
#     }

#     context = {
#         'weather_data': weather_data
#     }
#     return render(request, 'weather.html', context)


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


@login_required
def myposts(request):
    if request.method == 'GET':
        try:
            user_no = request.user.user_no  # 로그인된 사용자의 user_no 가져오기
            beach_no = request.GET.get('beach_no')  # 요청에서 beach_no 가져오기

            # beach_no에 따른 게시물 필터링
            if beach_no == 'common':
                event_boards = Event_board.objects.filter(user_no=user_no, beach_no__isnull=True)
            elif beach_no:
                event_boards = Event_board.objects.filter(user_no=user_no, beach_no=beach_no)
            else:
                event_boards = Event_board.objects.filter(user_no=user_no)
            
            # 페이징 처리
            paginator = Paginator(event_boards, 10)  # 페이지당 10개의 게시물
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            beaches = Beach.objects.all()

            return render(request, 'myposts.html', {'event_boards': event_boards, 'page_obj': page_obj, 'beaches': beaches, 'user': request.user})
        except AttributeError:
            # 로그인된 사용자가 없는 경우 처리
            return redirect('/')  # 로그인 페이지로 리디렉션
        except Event_board.DoesNotExist:
            # 일치하는 게시물이 없는 경우 처리
            return render(request, 'myposts.html', {'event_boards': [], 'user': request.user})
    else:
        return render(request, 'myposts.html')   
    
def agreement(request):
    # 내가 쓴 글을 가져오는 로직을 추가하세요.
    return render(request, 'agreement.html')

def team_info(request):
    return render(request, 'team_info.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def copyright(request):
    return render(request, 'copyright.html')

from django.shortcuts import render
from .utils import fetch_weather_data

def control_view(request):
    beach_no = request.GET.get('beach_no')
    
    beaches = Beach.objects.exclude(
        Q(beach_name="고래불 해수욕장") | 
        Q(beach_name="대천 해수욕장") | 
        Q(beach_name="함덕 해수욕장")
    )

    selected_beach = None
    weather_data = None
    widget_id = None

    if beach_no:
        try:
            beach = get_object_or_404(Beach, pk=beach_no)
            nx, ny = beach.nx, beach.ny
            selected_beach = beach.beach_name
            weather_data = fetch_weather_data({'nx': nx, 'ny': ny})
            widget_id = beach.beach_widget_id
        except (SyntaxError, KeyError):
            pass
    else:
        # Set default value to the first beach in the queryset
        first_beach = beaches.first()
        if first_beach:
            nx, ny = first_beach.nx, first_beach.ny
            selected_beach = first_beach.beach_name
            weather_data = fetch_weather_data({'nx': nx, 'ny': ny})
            widget_id = first_beach.beach_widget_id

    context = {
        'weather_data': weather_data,
        'beaches': beaches,
        'selected_beach': selected_beach,
        'widget_id': widget_id
    }
    
    return render(request, 'weather.html', context)
