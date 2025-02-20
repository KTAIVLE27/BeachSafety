from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
import json
from django.db.models import Q
import boto3
from django.conf import settings
import joblib
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from urllib.parse import quote
from django.shortcuts import render
import sqlite3
import pandas as pd
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from langchain.chains import RetrievalQA
from langchain.schema import Document
from django.shortcuts import render

from .utils import fetch_weather_data
from .utils import fetch_weather_data

from .models import *
from .forms import *
from control.utils import *

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(persist_directory="./database", embedding_function=embeddings)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=database.as_retriever(search_kwargs={"k": 20}),
    memory=memory
)


def is_admin(user):
    return user.is_authenticated and user.user_id == 'admin' and user.user_name == 'admin' and user.check_password('aivle2024!')

def forgotpw(request):
    return render(request, 'forgotpw.html')

@login_required
def admin_panel(request):
    return render(request, 'adminpanel/admin_home.html')

@login_required
def home(request):
    home_notices = Notice_board.objects.all().order_by('-notice_id')[:5]  
    home_event = Event_board.objects.all().order_by('-event_id')[:5] 
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
    context_json = json.dumps(context_rip)  
    combined_context = {
        **context,
        'context_rip_json': context_json  
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
            if search_type == 'all': 
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

# 파일 업로드 핸들러
def handle_uploaded_file(file, is_image=False):
    allowed_image_extensions = ['jpg', 'jpeg', 'png', 'gif']
    allowed_other_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'hwp', 'csv']
    max_file_size = 5 * 1024 * 1024  # 5MB

    ext = file.name.split('.')[-1].lower()
    if is_image:
        if ext not in allowed_image_extensions:
            raise ValueError("허용되지 않는 이미지 파일 형식입니다.")
    else:
        if ext not in allowed_other_extensions:
            raise ValueError("허용되지 않는 파일 형식입니다.")
    
    if file.size > max_file_size:
        raise ValueError("파일 크기가 너무 큽니다.")
    
    return True

@login_required
def board_detail(request, pk):
    try:
        post = Notice_board.objects.get(pk=pk)
        post.notice_views += 1  
        post.save()
    except Notice_board.DoesNotExist:
        messages.error(request, "해당 게시글을 찾을 수 없습니다.")
        return redirect('board')
    notice_img_filename = os.path.basename(post.notice_img) if post.notice_img else None
    notice_files = [(os.path.basename(file_url), file_url) for file_url in post.notice_files] if post.notice_files else None
    return render(request, 'board_detail.html', {'post': post, 'notice_img_filename':notice_img_filename, 'notice_files' :notice_files})

# 공지사항 이미지 다운로드
@login_required
def board_generate_presigned_url(request, pk):
    post = get_object_or_404(Notice_board, pk=pk)
    
    if not post.notice_img:
        return JsonResponse({'error': 'No image found.'}, status=404)

    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
    s3_key = post.notice_img.split(f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/')[1]
    filename = s3_key.split('/')[-1]
    encoded_filename = quote(filename)

    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': s3_bucket,
                'Key': s3_key,
                'ResponseContentDisposition': f'attachment; filename="{encoded_filename}"'
            },
            ExpiresIn=3600  # URL 유효 기간 (초)
        )
        return JsonResponse({'url': presigned_url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
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
            if search_type == 'all':
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
        post.event_views += 1  
        post.save()
    except Event_board.DoesNotExist:
        messages.error(request, "해당 게시글을 찾을 수 없습니다.")
        return redirect('free_board')
    beaches = Beach.objects.all()
    event_img_filename = os.path.basename(post.event_img) if post.event_img else None
    event_files = [(os.path.basename(file_url), file_url) for file_url in post.event_files] if post.event_files else None
    return render(request, 'freeboard_detail.html', {'post': post, 'beaches':beaches, 'event_img_filename': event_img_filename, 'event_files': event_files})

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
            
            if 'event_img' in request.FILES:
                file = request.FILES['event_img']
                
                if handle_uploaded_file(file, is_image = True):
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
                    
            other_files = []
            for file in request.FILES.getlist('other_files'):
                if handle_uploaded_file(file, is_image = False):
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        region_name=settings.AWS_S3_REGION_NAME
                    )
                    s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
                    s3_key = f'event/files/{file.name}'
                    s3.upload_fileobj(file, s3_bucket, s3_key, ExtraArgs={'ContentType': file.content_type})                                           
                    file_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}'
                    other_files.append(file_url)
                   
            event.evnet_files = other_files                                 
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
                
            if 'delete_event_img' in request.POST and request.POST['delete_event_img'] =='on':
                if post.event_img:
                    s3_key = post.event_img.split(f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/')[1]
                    s3.delete_object(Bucket=s3_bucket, Key=s3_key)
                event.event_img = None
                
            elif 'event_img' in request.FILES:
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
                existing_event_img = request.POST.get('existing_event_img')  # 기존 이미지 유지
                event.event_img = existing_event_img if existing_event_img else None
                
            
            other_files = event.event_files if event.event_files else []

            # 삭제할 파일 처리
            delete_files = request.POST.getlist('delete_other_files')
            for file_url in delete_files:
                if file_url in other_files:
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        region_name=settings.AWS_S3_REGION_NAME
                    )
                    s3_key = file_url.split(f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/')[1]
                    s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)
                    other_files.remove(file_url)

            # 새로운 파일 업로드 처리
            for file in request.FILES.getlist('other_files'):
                if handle_uploaded_file(file, is_image=False):
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        region_name=settings.AWS_S3_REGION_NAME
                    )
                    s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
                    s3_key = f'notices/files/{file.name}'
                    s3.upload_fileobj(file, s3_bucket, s3_key, ExtraArgs={'ContentType': file.content_type})

                    file_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}'
                    other_files.append(file_url)

            event.event_files = other_files                                 
            event.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'error': '잘못된 요청 방법입니다.'})

#자유게시판 삭제
@require_POST
def delete_freeboard(request, post_id):
    post = get_object_or_404(Event_board, pk=post_id, user_no=request.user)
    post.delete()
    return JsonResponse({'success': True})


# 자유게시판 이미지 다운로드
@login_required
def generate_presigned_url(request, pk):
    post = get_object_or_404(Event_board, pk=pk)
    
    if not post.event_img:
        return JsonResponse({'error': 'No image found.'}, status=404)

    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
    s3_key = post.event_img.split(f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/')[1]
    filename = s3_key.split('/')[-1]
    encoded_filename = quote(filename)

    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': s3_bucket,
                'Key': s3_key,
                'ResponseContentDisposition': f'attachment; filename="{encoded_filename}"'
            },
            ExpiresIn=3600  # URL 유효 기간 (초)
        )
        return JsonResponse({'url': presigned_url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
    beaches = Beach.objects.exclude(Q(beach_name="함덕 해수욕장"))
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

@csrf_exempt
def auto_admin_login(request):
    if request.method == 'POST':
        # 관리자 계정 정보
        admin_username = 'admin'
        admin_password = 'aivle202405!'
        # 관리자 계정 인증 및 로그인
        user = authenticate(request, username=admin_username, password=admin_password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

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
            user_no = request.user.user_no 
            beach_no = request.GET.get('beach_no')  

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
    return render(request, 'agreement.html')

def team_info(request):
    return render(request, 'team_info.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def copyright(request):
    return render(request, 'copyright.html')

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


# SQLite 데이터베이스에서 QA 데이터를 가져오는 함수 (새로 추가된 레코드만 가져오도록 수정)
def get_new_qa_data(last_id):
    conn = sqlite3.connect('db.sqlite3')
    query = f"SELECT scenario_qa FROM Scenario WHERE scenario_id > {last_id}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Embeddings 및 Chroma 데이터베이스 설정
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(persist_directory="./database", embedding_function=embeddings)

# QA 데이터를 Document 객체로 변환하고 Chroma 데이터베이스에 추가
def add_qa_to_database(last_id):
    data = get_new_qa_data(last_id)
    documents = [Document(page_content=text) for text in data['scenario_qa'].tolist()]
    database.add_documents(documents)

def chat(request):
    if request.method == 'POST':
        query = request.POST.get('question')

        chat = ChatOpenAI(model="gpt-3.5-turbo")
        k = 3
        retriever = database.as_retriever(search_kwargs={"k": k})
        qa = RetrievalQA.from_llm(llm=chat, retriever=retriever, return_source_documents=True)

        result = qa(query)
        answer = result["result"]

        timestamp = timezone.now()
        chatlog = Chatlog(question=query, answer=answer, created_at=timestamp)
        chatlog.save()

        logs = request.session.get('logs', [])
        logs.append({'question': query, 'answer': answer, 'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')})
        request.session['logs'] = logs

        return JsonResponse({'question': query, 'answer': answer, 'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')})
    else:
        logs = request.session.get('logs', [])
        return render(request, 'chat.html', {'logs': logs})

def chat_clear_logs(request):
    if request.method == 'POST':
        request.session['logs'] = []
        return redirect('chat')
    else:
        return HttpResponse(status=405)
    
    
def get_scenarios(request, scenario_type):
    if request.method == 'GET':
        scenario_type_map = {
            'biological_protection': '생물 보호',
            'water_leisure': '수상레저',
            'illegality': '불법',
            'marine_pollution': '해양오염',
            'safety_vacationers': '피서객 안전',
            'watery_man': '익수자',
            'medical_aid': '의료지원',
            'missing': '실종',
        }

        scenario_code = scenario_type_map.get(scenario_type)
        if not scenario_code:
            return JsonResponse({'error': 'Invalid scenario type'}, status=400)

        scenarios = Scenario.objects.filter(scenario_code=scenario_code).values('scenario_code', 'scenario_situation')
        scenario_list = list(scenarios)
        return JsonResponse({'scenarios': scenario_list})
    else:
        return HttpResponse(status=405)