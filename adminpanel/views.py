# from django.shortcuts import render
# from django.contrib.auth.models import User
# from main.models import User  # Ensure this is the correct import
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from main.models import *
from main.models import Event_board, Notice_board
from django.contrib import messages
import json
from main.forms import *
from django.db.models import Q
import csv
import io
from datetime import datetime
from main.utils import similarity_function 
import boto3
from django.conf import settings
from collections import Counter
from django.utils.timezone import localtime
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
    
    messages = []
    # Fetch all message codes from the database
    message_records = Message.objects.all()
    for record in message_records:
        details = fetch_message_details(record.message_code)
        if details:
            print("문자 기록!!:",details.text)
            messages.append(details)
        else :
            print("error!!!!!")
            
    
    return render(request, 'adminpanel/admin_home.html',
                  {'hours':hours, 'counts':counts, 'beaches': beaches, 
                   'user_count':user_count, 'beach_count':beach_count, 'board_count':board_count, 'notice_board_count':notice_board_count,'messages':messages})



def senario(request):
    # scenario_code 파라미터를 GET 요청에서 가져옴
    scenario_code = request.GET.get('scenario_code', '')

    # scenario_code가 존재하면 필터링된 시나리오 목록을 가져오고, 그렇지 않으면 모든 시나리오를 가져옴
    if scenario_code:
        scenario_list = Scenario.objects.filter(scenario_code=scenario_code)
    else:
        scenario_list = Scenario.objects.all()

    paginator = Paginator(scenario_list, 10)  # 한 페이지에 10개의 시나리오를 보여줌
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, 'adminpanel/senario.html', {'page_obj': page_obj, 'scenario_code': scenario_code})



def csv_upload(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            # 유효하지 않은 파일 유형 처리
            return render(request, 'csv_upload.html', {'error': 'CSV 파일이 아닙니다.'})
        
        file_data = csv_file.read().decode('utf-8-sig')  # 'utf-8-sig'로 BOM 처리
        csv_reader = csv.reader(io.StringIO(file_data))
        
        next(csv_reader)  # 첫 번째 행(헤더) 건너뛰기
        
        for row in csv_reader:
            if len(row) < 6:  # 모델의 필드 수에 맞게 조정
                continue
            
            try:
                # '시간' 데이터를 적절한 datetime 형식으로 변환
                scenario_time = datetime.strptime(row[2], '%H:%M')
            except ValueError:
                # 변환할 수 없는 경우 건너뜀
                continue
            
            Scenario.objects.create(
                scenario_code=row[1],
                scenario_time=scenario_time,
                scenario_situation=row[3],
                scenario_process=row[4],
                scenario_goals=row[5],
            )
        
        return redirect('adminpanel:senario')
    
    return render(request, 'adminpanel/csv_upload.html')

def delete_senario(request):
    try:
        data = json.loads(request.body)
        ids_to_delete = data['ids']
        Scenario.objects.filter(scenario_id__in=ids_to_delete).delete()
        return JsonResponse({"status": "success"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# 관리자
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
    
    return render(request, 'adminpanel/board_manage.html', {'posts': posts, 'page_obj': page_obj, 'beaches' : beaches})

@require_POST
def delete_boards(request):
    try:
        data = json.loads(request.body)
        ids_to_delete = data['ids']
        Event_board.objects.filter(event_id__in=ids_to_delete).delete()
        return JsonResponse({"status": "success"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
    

def user_list_view(request):
    users = User.objects.all().order_by('user_no')  # Order by 'user_no' or another appropriate field
    paginator = Paginator(users, 10)  # Show 10 users per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'adminpanel/user_list.html', context)

@csrf_exempt
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
    
    return render(request, 'adminpanel/notice_manage.html', {'posts': posts, 'beaches': beaches, 'selected_beach_no': beach_no, 'page_obj': page_obj})

@require_POST
def delete_notice_boards(request):
    try:
        data = json.loads(request.body)
        ids_to_delete = data['ids']
        print(ids_to_delete)
        Notice_board.objects.filter(notice_id__in=ids_to_delete).delete()
        return JsonResponse({"status": "success"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)



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
            
            # 파일 업로드 (client 방식)
            if 'notice_img' in request.FILES:
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
            notice.save()
            return redirect('adminpanel:notice_manage')
    else:
        form = PostForm()
    beaches = Beach.objects.all()
    return render(request, 'adminpanel/create_notice.html', {'beaches': beaches})


@login_required
def notice_detail(request, pk):
    try:
        post = Notice_board.objects.get(pk=pk)
        post.save()
    except Notice_board.DoesNotExist:
        messages.error(request, "해당 게시글을 찾을 수 없습니다.")
        return redirect('adminpanel:notice_manage')
    
    beaches = Beach.objects.all()
    return render(request, 'adminpanel/notice_detail.html', {'post': post, 'beaches':beaches})

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
                
            # 파일 업로드 (client 방식)
            if 'notice_img' in request.FILES:
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
                notice.notice_img = request.POST.get('existing_notice_img')  # 기존 이미지 유지               
            notice.save()
            return JsonResponse({'success': True})
        else:
            # 폼이 유효하지 않은 경우 오류 메시지를 반환
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})

    return JsonResponse({'success': False, 'error': '잘못된 요청 방법입니다.'})


@login_required
def board_detail(request, pk):
    try:
        post = Event_board.objects.get(pk=pk)
        post.save()
    except Event_board.DoesNotExist:
        messages.error(request, "해당 게시글을 찾을 수 없습니다.")
        return redirect('adminpanel:board_manage')
    
    return render(request, 'adminpanel/board_detail.html', {'post': post})

def control_load(request):
    return render(request, 'control.html')

def main_load(request):
    return render(request, 'home.html')

# import os
# import time
# import datetime
# import uuid
# import hmac
# import hashlib
# import requests

# # Define the necessary functions
# def unique_id():
#     return str(uuid.uuid1().hex)

# def get_iso_datetime():
#     utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
#     utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
#     return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

# def get_signature(key, msg):
#     return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

# def get_headers(apiKey, apiSecret):
#     date = get_iso_datetime()
#     salt = unique_id()
#     data = date + salt
#     signature = get_signature(apiSecret, data)
#     headers = {
#         'Authorization': f'HMAC-SHA256 ApiKey={apiKey}, Date={date}, salt={salt}, signature={signature}',
#         'Content-Type': 'application/json'
#     }
#     return headers

# # Environment variables for API key and secret
# MESSAGE_API_KEY = os.getenv('MESSAGE_API_KEY')
# MESSAGE_API_SECRET = os.getenv('MESSAGE_API_SECRET')

# # Choose a specific messageId from the list
# message_id = "M4V20240716133457QFCYT7I7A4R9XCP"  # Replace with any valid messageId from your list

# # URL for the API request to get the specific message details
# url = f"http://api.coolsms.co.kr/messages/v4/list?criteria=messageId&value={message_id}&cond=eq"

# # Generate headers
# headers = get_headers(MESSAGE_API_KEY, MESSAGE_API_SECRET)

# # Make the request
# response = requests.get(url, headers=headers)

# # Print the response status and body
# print(response.status_code)
# print(response.json())

# import os
# import time
# import datetime
# import uuid
# import hmac
# import hashlib
# import requests

# # Define the necessary functions
# def unique_id():
#     return str(uuid.uuid1().hex)

# def get_iso_datetime():
#     utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
#     utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
#     return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

# def get_signature(key, msg):
#     return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

# def get_headers(apiKey, apiSecret):
#     date = get_iso_datetime()
#     salt = unique_id()
#     data = date + salt
#     signature = get_signature(apiSecret, data)
#     headers = {
#         'Authorization': f'HMAC-SHA256 ApiKey={apiKey}, Date={date}, salt={salt}, signature={signature}',
#         'Content-Type': 'application/json'
#     }
#     return headers

# # Environment variables for API key and secret
# MESSAGE_API_KEY = os.getenv('MESSAGE_API_KEY')
# MESSAGE_API_SECRET = os.getenv('MESSAGE_API_SECRET')

# # Choose a specific messageId from the list
# message_id = "M4V20240716133457QFCYT7I7A4R9XCP"  # Replace with any valid messageId from your list

# # URL for the API request to get the specific message details
# url = f"http://api.coolsms.co.kr/messages/v4/list?criteria=messageId&value={message_id}&cond=eq"

# # Generate headers
# headers = get_headers(MESSAGE_API_KEY, MESSAGE_API_SECRET)

# # Make the request
# response = requests.get(url, headers=headers)

# # Print the response status and body
# print(response.status_code)

# # Parse the response JSON
# response_json = response.json()

# # Extract and print specific fields
# if 'messageList' in response_json and response_json['messageList']:
#     message_details = response_json['messageList'].get(message_id)
#     if message_details:
#         text = message_details.get('text')
#         from_number = message_details.get('from')
#         deliver_date = None
#         for log in message_details.get('log', []):
#             if 'originalData' in log and 'DELIVER_DATE' in log['originalData']:
#                 deliver_date = log['originalData']['DELIVER_DATE']
#                 break
#         print(f"messageId: {message_id}")
#         print(f"text: {text}")
#         print(f"DELIVER_DATE: {deliver_date}")
#         print(f"from: {from_number}")
# else:
#     print("No message details found.")
    
# import os
# import time
# import datetime
# import uuid
# import hmac
# import hashlib
# import requests
# from django.shortcuts import render
# from django.conf import settings

# # Define the necessary functions
# def unique_id():
#     return str(uuid.uuid1().hex)

# def get_iso_datetime():
#     utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
#     utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
#     return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

# def get_signature(key, msg):
#     return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

# def get_headers(apiKey, apiSecret):
#     date = get_iso_datetime()
#     salt = unique_id()
#     data = date + salt
#     signature = get_signature(apiSecret, data)
#     headers = {
#         'Authorization': f'HMAC-SHA256 ApiKey={apiKey}, Date={date}, salt={salt}, signature={signature}',
#         'Content-Type': 'application/json'
#     }
#     return headers

# def fetch_messages():
#     # Environment variables for API key and secret
#     MESSAGE_API_KEY = os.getenv('MESSAGE_API_KEY')
#     MESSAGE_API_SECRET = os.getenv('MESSAGE_API_SECRET')

#     # URL for the API request to get message list
#     url = "http://api.coolsms.co.kr/messages/v4/list"

#     # Generate headers
#     headers = get_headers(MESSAGE_API_KEY, MESSAGE_API_SECRET)

#     # Make the request to get the list of messages
#     response = requests.get(url, headers=headers)

#     # Print the response status and body
#     print(response.status_code)
#     response_json = response.json()
#     print(response_json)

#     messages = []

#     # Extract and save message IDs if available
#     if 'messageList' in response_json and response_json['messageList']:
#         for message_id, details in response_json['messageList'].items():
#             text = details.get('text')
#             from_number = details.get('from')
#             deliver_date = None
#             for log in details.get('log', []):
#                 if 'originalData' in log and 'DELIVER_DATE' in log['originalData']:
#                     deliver_date = log['originalData']['DELIVER_DATE']
#                     break
#             messages.append({
#                 'messageId': message_id,
#                 'text': text,
#                 'from': from_number,
#                 'deliver_date': deliver_date
#             })
#     return messages

# def admin_home(request):
#     messages = fetch_messages()
#     return render(request, 'adminpanel/admin_home.html', {'messages': messages})

# import os
# import time
# import datetime
# import uuid
# import hmac
# import hashlib
# import requests
# import django
# from django.conf import settings

# # Setup Django settings
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
# django.setup()

# # Define the necessary functions
# def unique_id():
#     return str(uuid.uuid1().hex)

# def get_iso_datetime():
#     utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
#     utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
#     return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

# def get_signature(key, msg):
#     return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

# def get_headers(apiKey, apiSecret):
#     date = get_iso_datetime()
#     salt = unique_id()
#     data = date + salt
#     signature = get_signature(apiSecret, data)
#     headers = {
#         'Authorization': f'HMAC-SHA256 ApiKey={apiKey}, Date={date}, salt={salt}, signature={signature}',
#         'Content-Type': 'application/json'
#     }
#     return headers

# # Environment variables for API key and secret
# MESSAGE_API_KEY = os.getenv('MESSAGE_API_KEY')
# MESSAGE_API_SECRET = os.getenv('MESSAGE_API_SECRET')

# # URL for the API request to get message list
# url = "http://api.coolsms.co.kr/messages/v4/list"

# # Generate headers
# headers = get_headers(MESSAGE_API_KEY, MESSAGE_API_SECRET)

# # Make the request to get the list of messages
# response = requests.get(url, headers=headers)

# # Print the response status and body
# print(response.status_code)
# response_json = response.json()
# print(response_json)

# # Extract and save message IDs if available
# if 'messageList' in response_json and response_json['messageList']:
#     for message_id in response_json['messageList']:
#         print("Found messageId:", message_id)
#         # Save the messageId to the database
#         Message.objects.create(message_code=message_id)
# else:
#     print("No messages found.")

import os
import time
import datetime
import uuid
import hmac
import hashlib
import requests
from django.shortcuts import render
from main.models import Message

# Define the necessary functions
def unique_id():
    return str(uuid.uuid1().hex)

def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

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

def fetch_message_details(message_code):
    # Environment variables for API key and secret
    MESSAGE_API_KEY = os.getenv('MESSAGE_API_KEY')
    MESSAGE_API_SECRET = os.getenv('MESSAGE_API_SECRET')

    # URL for the API request to get message details
    url = "http://api.coolsms.co.kr/messages/v4/list"

    # Generate headers
    headers = get_headers(MESSAGE_API_KEY, MESSAGE_API_SECRET)

    # Make the request to get the message details
    params = {
        'groupId' : message_code
    }
    response = requests.get(url, headers=headers, params=params)
    print("문자기록함수:", response)

    # Print the response status and body
    #print(response.status_code)
    response_json = response.json()
    #print(response_json)

    if 'messageList' in response_json and response_json['messageList']:
        print( response_json['messageList'])
        message_details = response_json['messageList'].get(message_code)
        print("여기 if 문!!!1:", message_details)
        if message_details:
            text = message_details.get('text')
            print("문자 가져와야함!!:",text)
            from_number = message_details.get('from')
            deliver_date = None
            for log in message_details.get('log', []):
                if 'originalData' in log and 'DELIVER_DATE' in log['originalData']:
                    deliver_date = log['originalData']['DELIVER_DATE']
                    break
            return {
                'messageId': message_code,
                'text': text,
                'from': from_number,
                'deliver_date': deliver_date
            }
    return None



# import os
# import time
# import datetime
# import uuid
# import hmac
# import hashlib
# import requests

# # Define the necessary functions
# def unique_id():
#     return str(uuid.uuid1().hex)

# def get_iso_datetime():
#     utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
#     utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
#     return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

# def get_signature(key, msg):
#     return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

# def get_headers(apiKey, apiSecret):
#     date = get_iso_datetime()
#     salt = unique_id()
#     data = date + salt
#     signature = get_signature(apiSecret, data)
#     headers = {
#         'Authorization': f'HMAC-SHA256 ApiKey={apiKey}, Date={date}, salt={salt}, signature={signature}',
#         'Content-Type': 'application/json'
#     }
#     return headers

# # Environment variables for API key and secret
# MESSAGE_API_KEY = os.getenv('MESSAGE_API_KEY')
# MESSAGE_API_SECRET = os.getenv('MESSAGE_API_SECRET')

# # URL for the API request to get message list


# # Generate headers
# headers = get_headers(MESSAGE_API_KEY, MESSAGE_API_SECRET)

# # Request parameters


# # Send the GET request
# response = requests.get(url, headers=headers, params=params)

# # Handle the response
# if response.status_code == 200:
#     # Successfully retrieved data
#     data = response.json()
#     print("Messages:", data)
# else:
#     # Error occurred
#     print("Error:", response.status_code, response.text)

