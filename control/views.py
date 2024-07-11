from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
# ['GYEONGPO', 'GORAEBUL','NAKSAN','DAECHON','MANGSANG','SOKCHO','SONGJUNG','IMRANG','JUNGMUN','HAE']

from .utils import *
import json
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
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)  # JSON 응답 반환
    else:
        context_json = json.dumps(context)  # JSON 형식의 문자열로 변환
        return render(request, 'control.html', {'contextjson': context_json})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

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

        # 4 params(to, from, type, text) are mandatory. must be filled
        params = dict()
        params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
        params['to'] = '01033634184' # Recipients Number
        params['from'] = '01033634184' # Sender number
        params['text'] = f'{beach_name} 신고가 접수되었습니다.' # Message

        cool = Message(MESSAGE_API_KEY, MESSAGE_API_SECRET)
        try:
            response = cool.send(params)
            return JsonResponse({'status': 'success', 'response': response})
        except CoolsmsException as e:
            return JsonResponse({'status': 'error', 'code': e.code, 'message': e.msg})
    return JsonResponse({'status': 'invalid request'}, status=400)


