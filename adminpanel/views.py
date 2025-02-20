from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import csv
import io
import boto3
from django.conf import settings
from collections import Counter
from django.db.models import Q
from django.utils.timezone import localtime
import time 
import hmac
import hashlib
import uuid
import requests
import os
import datetime
from datetime import datetime, timedelta
from datetime import timezone as dt_timezone  
from django.utils import timezone
from .utils import mask_user_data
from urllib.parse import quote

from main.views import add_qa_to_database
from main.forms import *
from main.models import *

def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

def unique_id():
    return str(uuid.uuid1().hex)

def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = timedelta(seconds=-utc_offset_sec)
    return datetime.now().replace(tzinfo=dt_timezone(offset=utc_offset)).isoformat()

def get_headers(apiKey, apiSecret):
    date = get_iso_datetime()
    salt = unique_id()
    data = date + salt
    signature = get_signature(apiSecret, data)
    headers = {
        'Authorization': f'HMAC-SHA256 ApiKey={apiKey}, Date={date}, salt={salt}, signature={signature}',
        'Content-Type': 'application/json'
    }
    return headers

def format_date(date_string):
    if date_string is None:
        return None
    date_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=dt_timezone.utc)
    kst = dt_timezone(timedelta(hours=9))
    local_date_obj = date_obj.astimezone(kst)
    return local_date_obj.strftime('%Y-%m-%d %H:%M:%S')

def fetch_message_details(message_code):
    MESSAGE_API_KEY = os.getenv('MESSAGE_API_KEY')
    MESSAGE_API_SECRET = os.getenv('MESSAGE_API_SECRET')

    url = f"http://api.coolsms.co.kr/messages/v4/list?criteria=messageId&value={message_code}&cond=eq"
    headers = get_headers(MESSAGE_API_KEY, MESSAGE_API_SECRET)

    response = requests.get(url, headers=headers)

    response_json = response.json()
    if 'messageList' in response_json and response_json['messageList']:
        message_list = response_json.get('messageList', {})
        extracted_messages = []
        for message_id, message_data in message_list.items():
            text = message_data.get('text')
            from_number = message_data.get('from')
            deliver_date = message_data.get('dateReceived')
            if text and deliver_date:
                extracted_messages.append({
                    'text': text,
                    'from': from_number,
                    'deliver_date': format_date(deliver_date)
                })
            return extracted_messages

    return None

@login_required
def admin_home(request):

    beaches = Beach.objects.all()
    beach_count = Beach.objects.count()
    user_count = User.objects.count()
    board_count = Event_board.objects.count()
    notice_board_count = Notice_board.objects.count()
    
    last_logins = User.objects.values_list('last_login', flat=True)

    login_count = Counter()

    
    for login_time in last_logins:
        local_login_time = localtime(login_time)
        if local_login_time:
            hour = local_login_time.hour
            login_count[hour] +=1
    
    hours = list(range(24))
    counts = [login_count[hour] for hour in hours]
    
    
    message_codes = Message.objects.values_list('message_code', flat=True)
    messages = []
    for message_code in message_codes:
        message_details = fetch_message_details(message_code)
        if isinstance(message_details, list):
            messages.extend(message_details)
        else:
            messages.append(message_details)
    
    sorted_messages = sorted(messages, key=lambda x: x.get('deliver_date', ''), reverse=True)
    return render(request, 'adminpanel/admin_home.html',
                  {'hours':hours, 'counts':counts, 'beaches': beaches, 
                   'user_count':user_count, 'beach_count':beach_count,
                   'board_count':board_count, 'notice_board_count':notice_board_count,
                   'messages':sorted_messages
                   })


@login_required
def senario(request):
    scenario_code = request.GET.get('scenario_code', '')

    if scenario_code:
        scenario_list = Scenario.objects.filter(scenario_code=scenario_code)
    else:
        scenario_list = Scenario.objects.all()

    paginator = Paginator(scenario_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, 'adminpanel/senario.html', {'page_obj': page_obj, 'scenario_code': scenario_code})



# CSV 업로드 핸들러
@login_required
def csv_upload(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return render(request, 'csv_upload.html', {'error': 'CSV 파일이 아닙니다.'})
        
        file_data = csv_file.read().decode('utf-8-sig')
        csv_reader = csv.reader(io.StringIO(file_data))
        next(csv_reader)  # 첫 번째 행(헤더) 건너뛰기
        
        # 현재 마지막 ID 저장
        last_id = Scenario.objects.latest('scenario_id').scenario_id if Scenario.objects.exists() else 0
        
        for row in csv_reader:
            if len(row) < 6:
                continue
            
            try:
                scenario_time = datetime.strptime(row[2], '%H:%M')
            except ValueError:
                continue
            
            Scenario.objects.create(
                scenario_code=row[1],
                scenario_time=scenario_time,
                scenario_situation=row[3],
                scenario_process=row[4],
                scenario_goals=row[5],
                scenario_qa=row[6]
            )
        
        add_qa_to_database(last_id)
        return redirect('adminpanel:senario')
    
    return render(request, 'adminpanel/csv_upload.html')

@login_required
def delete_senario(request):
    try:
        data = json.loads(request.body)
        ids_to_delete = data['ids']
        Scenario.objects.filter(scenario_id__in=ids_to_delete).delete()
        return JsonResponse({"status": "success"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# 자유게시판
@login_required
def board_manage(request):    
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
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    beaches = Beach.objects.all()
    
    return render(request, 'adminpanel/board_manage.html', {'posts': posts, 'page_obj': page_obj, 'beaches' : beaches})

@require_POST
@login_required
def delete_boards(request):
    try:
        data = json.loads(request.body)
        ids_to_delete = data['ids']
        Event_board.objects.filter(event_id__in=ids_to_delete).delete()
        return JsonResponse({"status": "success"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
@login_required
def user_list_view(request):
    users = User.objects.all().order_by('user_no') 
    masked_users = [mask_user_data(user) for user in users]
    paginator = Paginator(masked_users, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'adminpanel/user_list.html', context)

@login_required
def user_detail(request, user_no):
    user_info = User.objects.get(user_no=user_no)
    return render(request, 'adminpanel/user_detail.html', {'user_info': user_info})

@csrf_exempt
@login_required
def delete_users(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('ids[]')
        if user_ids:
            User.objects.filter(user_no__in=user_ids).delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'no ids provided'}, status=400)
    return JsonResponse({'status': 'invalid request'}, status=400)

# 공지사항
@login_required
def notice_manage(request):
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
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    beaches = Beach.objects.all()
    
    return render(request, 'adminpanel/notice_manage.html', {'posts': posts, 'beaches': beaches, 'selected_beach_no': beach_no, 'page_obj': page_obj})

@require_POST
def delete_notice_boards(request):
    try:
        data = json.loads(request.body)
        ids_to_delete = data['ids']
        Notice_board.objects.filter(notice_id__in=ids_to_delete).delete()
        return JsonResponse({"status": "success"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

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
def create_notice(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user_no = request.user
            notice.notice_wdate = timezone.now()
            if not notice.beach_no:
                notice.beach_no = None
            
            # 파일 업로드 (image)
            if 'notice_img' in request.FILES:
                file = request.FILES['notice_img']
                
                if handle_uploaded_file(file, is_image = True):
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        region_name=settings.AWS_S3_REGION_NAME
                    )
                    
                    s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
                    s3_key = f'notices/{file.name}'
                    s3.upload_fileobj(file, s3_bucket, s3_key, ExtraArgs={'ContentType': file.content_type})
                    
                    file_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}'
                    notice.notice_img = file_url
                    
            other_files = []
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
 
            notice.notice_files = other_files                        
            notice.save()
            return redirect('adminpanel:notice_manage')
    else:
        form = PostForm()
    beaches = Beach.objects.all()
    return render(request, 'adminpanel/create_notice.html', {'form': form, 'beaches': beaches})


@login_required
def notice_detail(request, pk):
    try:
        post = Notice_board.objects.get(pk=pk)
        post.save()
    except Notice_board.DoesNotExist:
        messages.error(request, "해당 게시글을 찾을 수 없습니다.")
        return redirect('adminpanel:notice_manage')
    
    beaches = Beach.objects.all()
    notice_img_filename = os.path.basename(post.notice_img) if post.notice_img else None
    notice_files = [(os.path.basename(file_url), file_url) for file_url in post.notice_files] if post.notice_files else None
    return render(request, 'adminpanel/notice_detail.html', {'post': post, 'beaches':beaches, 'notice_img_filename': notice_img_filename, 'notice_files':notice_files})

@login_required
def edit_notice(request, pk):
    post = get_object_or_404(Notice_board, pk=pk)

    # 작성자 검증
    if request.user != post.user_no and request.user.role != 'admin':
        return JsonResponse({'success': False, 'error': '권한이 없습니다.'})

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            notice = form.save(commit=False)
            if notice.beach_no == '':
                notice.beach_no = None

            if 'delete_notice_img' in request.POST and request.POST['delete_notice_img'] == 'on':
                if post.notice_img:
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        region_name=settings.AWS_S3_REGION_NAME
                    )
                    s3_key = post.notice_img.split(f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/')[1]
                    s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)
                notice.notice_img = None
                
            elif 'notice_img' in request.FILES:
                file = request.FILES['notice_img']

                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )

                s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
                s3_key = f'notices/{file.name}'
                s3.upload_fileobj(file, s3_bucket, s3_key, ExtraArgs={'ContentType': file.content_type})

                file_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}'
                notice.notice_img = file_url
            else:
                existing_notice_img = request.POST.get('existing_notice_img')
                notice.notice_img = existing_notice_img if existing_notice_img else None

            # 기타 파일 처리
            other_files = notice.notice_files if notice.notice_files else []

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

            notice.notice_files = other_files
            notice.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})

    return JsonResponse({'success': False, 'error': '잘못된 요청 방법입니다.'})

# 이미지 다운로드
@login_required
def generate_presigned_url(request, pk):
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
def board_detail(request, pk):
    try:
        post = Event_board.objects.get(pk=pk)
        post.save()
    except Event_board.DoesNotExist:
        messages.error(request, "해당 게시글을 찾을 수 없습니다.")
        return redirect('adminpanel:board_manage')
    event_img_filename = os.path.basename(post.event_img) if post.event_img else None
    event_files = [(os.path.basename(file_url), file_url) for file_url in post.event_files] if post.event_files else None
    return render(request, 'adminpanel/board_detail.html', {'post': post, 'event_img_filename':event_img_filename ,'event_files': event_files})

@login_required
def control_load(request):
    return render(request, 'control.html')

@login_required
def main_load(request):
    return render(request, 'home.html')

