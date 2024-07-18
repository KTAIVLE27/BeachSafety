from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from main.models import Message as MessageModel
import time 
import hmac
import hashlib
import uuid
import requests
import datetime
# Create your views here.
# ['GYEONGPO', 'GORAEBUL','NAKSAN','DAECHON','MANGSANG','SOKCHO','SONGJUNG','IMRANG','JUNGMUN','HAE']

from .utils import *
import json
from main.models import *
def control_view(request):
    context = {
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
        
        'RIP_api_time': get_beach_obs_time('HAE'),

        
    }
    beaches = Beach.objects.all()
    cctvs = CCTV.objects.select_related('beach_no')
    api_key = os.getenv('WEATHER_API_2')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)  # JSON 응답 반환
    else:
        context_json = json.dumps(context)  # JSON 형식의 문자열로 변환
        return render(request, 'control.html', {'contextjson': context_json, 'beaches': beaches, 'cctvs': cctvs, 'api_key' :api_key})

def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

def unique_id():
    return str(uuid.uuid1().hex)

from datetime import timedelta, datetime, timezone

def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = timedelta(seconds=-utc_offset_sec)
    return datetime.now().replace(tzinfo=timezone(offset=utc_offset)).isoformat()


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

@csrf_exempt
def send_sms(request):
    if request.method == 'POST':
        # set api key, api secret
        MESSAGE_API_KEY = os.getenv('MESSAGE_API_KEY')
        MESSAGE_API_SECRET = os.getenv('MESSAGE_API_SECRET')

        if not MESSAGE_API_KEY or not MESSAGE_API_SECRET:
            return JsonResponse({'status': 'error', 'message': 'API key or secret not set'}, status=400)

        # Get beach name from request
        beach_name = request.POST.get('beach_name')
        if not beach_name:
            return JsonResponse({'status': 'error', 'message': 'Beach name not provided'}, status=400)

        data = {
            "message": {
                "to": "01033634184",
                "from": "01033634184",
                "text": f"{beach_name} 신고가 접수되었습니다.",
                "type": "SMS"
            }
        }
        
        data_json = json.dumps(data, ensure_ascii=False).encode('utf-8')

        url = "http://api.coolsms.co.kr/messages/v4/send"
        headers = get_headers(MESSAGE_API_KEY, MESSAGE_API_SECRET)
        
        try:
            response = requests.post(url, headers=headers, data=data_json)
            response_data = response.json()
            message_code = response_data.get('messageId')

            if message_code:
                MessageModel.objects.create(message_code=message_code)
                return JsonResponse({'status': 'success', 'response': response_data})
            else:
                return JsonResponse({'status': 'error', 'message': 'Message ID not found in response'}, status=500)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'invalid request'}, status=400)

# yolo 모델 적용
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
import cv2
import numpy as np
import yt_dlp as youtube_dl
from ultralytics import YOLO
from threading import Event

# YOLOv8 모델 설정
model = YOLO('control/best3.pt')  # 세그멘테이션 모델 파일 경로

human_detected = False
general_count = 0 # 사람 수 세기
cacution_count = 0 # 주의 요먕 인원 세기

# 함덕 해수욕장
def stream_video(video_url, cctv_code):
    global stop_stream_event, human_detected, general_count, cacution_count
    
    if cctv_code == 1:
        stop_stream_event.clear()

        ydl_opts = {
            'format': 'best',
            'quiet': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_url = info_dict['url']

        cap = cv2.VideoCapture(video_url)
        classes = model.names
        print(classes)  # 디버깅을 위해 추가
        sea_class_index = None
        human_class_index = None
        for i, class_name in enumerate(classes):
            if class_name == 1:  # 클래스 이름을 모델에 맞게 수정
                sea_class_index = i
            elif class_name == 0:  # 클래스 이름을 모델에 맞게 수정
                human_class_index = i
            if sea_class_index is not None and human_class_index is not None:
                break

        if sea_class_index is None:
            raise ValueError("The 'sea' class was not found in the model classes.")
        if human_class_index is None:
            raise ValueError("The 'human' class was not found in the model classes.")


        offset1 = 100
        offset2 = 50


        while cap.isOpened():
            if stop_stream_event.is_set():
                break

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 360))
            results = model.predict(source=frame, save=False, show=False)
            annotated_frame = results[0].plot()
            human_detected = False
            sea_box = None

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls)
                    if cls == sea_class_index:
                        sea_box = box
                        break

            if sea_box is not None:
                x1, y1, x2, y2 = map(int, sea_box.xyxy[0])

                adjusted_y1 = y2 - offset1


                start_point1 = (0, adjusted_y1)
                end_point1 = (640, adjusted_y1)
                color1 = (255, 0, 0)
                thickness = 2
                cv2.line(annotated_frame, start_point1, end_point1, color1, thickness)


                adjusted_y2 = y2 - offset2

                start_point2 = (0, adjusted_y2)
                end_point2 = (640, adjusted_y2)
                color2 = (0, 255, 0)
                thickness = 2
                cv2.line(annotated_frame, start_point2, end_point2, color2, thickness)

                general_count = 0 # 사람 수 세기
                cacution_count = 0 # 주의 요먕 인원 세기
                # 사람의 바운딩 박스를 주황색으로 변경

                for box in boxes:
                    cls = int(box.cls)
                    if cls == human_class_index:
                        hx1, hy1, hx2, hy2 = map(int, box.xyxy[0])
                        if hy2 < adjusted_y2:
                            color_human = (0, 165, 255)
                            cv2.rectangle(annotated_frame, (hx1, hy1), (hx2, hy2), color_human, 2)

                            human_detected = True
                            cacution_count+=1
                        else:
                            general_count+=1
                            
                # 출력문은 모달창에 사람 수 변수로 넘긴 후 삭제 예정
                # 파란색, 주황색 바운딩 박스의 사람 수 출력
                print(f"Number of general people: {general_count}")
                print(f"Number of cacution people: {cacution_count}")


            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()
        
    elif cctv_code == 2:
        stop_stream_event.clear()

        ydl_opts = {
            'format': 'best',
            'quiet': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_url = info_dict['url']

        cap = cv2.VideoCapture(video_url)
        classes = model.names
        print(classes)  # 디버깅을 위해 추가
        
        sea_class_index = None
        human_class_index = None
        for i, class_name in enumerate(classes):
            if class_name == 1:  # 클래스 이름을 모델에 맞게 수정
                sea_class_index = i
            elif class_name == 0:  # 클래스 이름을 모델에 맞게 수정
                human_class_index = i
            if sea_class_index is not None and human_class_index is not None:
                break

        if sea_class_index is None:
            raise ValueError("The 'sea' class was not found in the model classes.")
        if human_class_index is None:
            raise ValueError("The 'human' class was not found in the model classes.")

        offset1 = 300 # blue
        offset2 = 200 # green

        while cap.isOpened():
            if stop_stream_event.is_set():
                break

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 360))
            results = model.predict(source=frame, save=False, show=False)
            annotated_frame = results[0].plot()
            human_detected = False
            sea_box = None

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls)
                    if cls == sea_class_index:
                        sea_box = box
                        break

            if sea_box is not None:
                x1, y1, x2, y2 = map(int, sea_box.xyxy[0])

                adjusted_y1 = y2 - offset1
                start_point1 = (adjusted_y1, 0)
                end_point1 = (adjusted_y1, 640)
                color1 = (255, 0, 0)
                thickness = 2
                cv2.line(annotated_frame, start_point1, end_point1, color1, thickness)


                adjusted_y2 = y2 - offset2

                start_point2 = (adjusted_y2, 0)
                end_point2 = (adjusted_y2, 640)
                color2 = (0, 255, 0)
                thickness = 2
                cv2.line(annotated_frame, start_point2, end_point2, color2, thickness)

                general_count = 0 # 사람 수 세기
                cacution_count = 0 # 주의 요먕 인원 세기
                # 사람의 바운딩 박스를 주황색으로 변경

                for box in boxes:
                    cls = int(box.cls)
                    if cls == human_class_index:
                        hx1, hy1, hx2, hy2 = map(int, box.xyxy[0])
                        if hy2 < adjusted_y2:
                            color_human = (0, 165, 255)
                            cv2.rectangle(annotated_frame, (hx1, hy1), (hx2, hy2), color_human, 2)

                            human_detected = True
                            cacution_count+=1
                        else:
                            general_count+=1
                            
                # 출력문은 모달창에 사람 수 변수로 넘긴 후 삭제 예정
                # 파란색, 주황색 바운딩 박스의 사람 수 출력
                print(f"Number of general people: {general_count}")
                print(f"Number of cacution people: {cacution_count}")


            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()

# # 중문 해수욕장
# def stream_video2(video_url):
#     global stop_stream_event, human_detected, general_count, cacution_count
#     stop_stream_event.clear()

#     ydl_opts = {
#         'format': 'best',
#         'quiet': True
#     }

#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(video_url, download=False)
#         video_url = info_dict['url']

#     cap = cv2.VideoCapture(video_url)
#     classes = model.names
#     print(classes)  # 디버깅을 위해 추가
    
#     sea_class_index = None
#     human_class_index = None
#     for i, class_name in enumerate(classes):
#         if class_name == 1:  # 클래스 이름을 모델에 맞게 수정
#             sea_class_index = i
#         elif class_name == 0:  # 클래스 이름을 모델에 맞게 수정
#             human_class_index = i
#         if sea_class_index is not None and human_class_index is not None:
#             break

#     if sea_class_index is None:
#         raise ValueError("The 'sea' class was not found in the model classes.")
#     if human_class_index is None:
#         raise ValueError("The 'human' class was not found in the model classes.")

#     offset1 = 300 # blue
#     offset2 = 200 # green

#     while cap.isOpened():
#         if stop_stream_event.is_set():
#             break

#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame = cv2.resize(frame, (640, 360))
#         results = model.predict(source=frame, save=False, show=False)
#         annotated_frame = results[0].plot()
#         human_detected = False
#         sea_box = None

#         for result in results:
#             boxes = result.boxes
#             for box in boxes:
#                 cls = int(box.cls)
#                 if cls == sea_class_index:
#                     sea_box = box
#                     break

#         if sea_box is not None:
#             x1, y1, x2, y2 = map(int, sea_box.xyxy[0])

#             adjusted_y1 = y2 - offset1
#             start_point1 = (adjusted_y1, 0)
#             end_point1 = (adjusted_y1, 640)
#             color1 = (255, 0, 0)
#             thickness = 2
#             cv2.line(annotated_frame, start_point1, end_point1, color1, thickness)


#             adjusted_y2 = y2 - offset2

#             start_point2 = (adjusted_y2, 0)
#             end_point2 = (adjusted_y2, 640)
#             color2 = (0, 255, 0)
#             thickness = 2
#             cv2.line(annotated_frame, start_point2, end_point2, color2, thickness)

#             general_count = 0 # 사람 수 세기
#             cacution_count = 0 # 주의 요먕 인원 세기
#             # 사람의 바운딩 박스를 주황색으로 변경

#             for box in boxes:
#                 cls = int(box.cls)
#                 if cls == human_class_index:
#                     hx1, hy1, hx2, hy2 = map(int, box.xyxy[0])
#                     if hy2 < adjusted_y2:
#                         color_human = (0, 165, 255)
#                         cv2.rectangle(annotated_frame, (hx1, hy1), (hx2, hy2), color_human, 2)

#                         human_detected = True
#                         cacution_count+=1
#                     else:
#                         general_count+=1
                        
#             # 출력문은 모달창에 사람 수 변수로 넘긴 후 삭제 예정
#             # 파란색, 주황색 바운딩 박스의 사람 수 출력
#             print(f"Number of general people: {general_count}")
#             print(f"Number of cacution people: {cacution_count}")


#         ret, buffer = cv2.imencode('.jpg', annotated_frame)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     cap.release()


def video_feed(request, cctv_code):
    cctv = CCTV.objects.get(cctv_code=cctv_code)
    video_url = cctv.cctv_url
    
    return StreamingHttpResponse(stream_video(video_url, cctv_code),
                                content_type='multipart/x-mixed-replace; boundary=frame')

def human_status(request, cctv_code):
    return JsonResponse({'human_detected': human_detected,
                         'general_count':general_count,
                         'cacution_count':cacution_count,})


stop_stream_event = Event()
def stop_stream(request):
    global stop_stream_event
    stop_stream_event.set()
    return JsonResponse({'status': 'stopped'})