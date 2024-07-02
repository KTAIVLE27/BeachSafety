from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.





# ['GYEONGPO', 'GORAEBUL','NAKSAN','DAECHON','MANGSANG','SOKCHO','SONGJUNG','IMRANG','JUNGMUN','HAE']

from .utils import *
import json
def control_view(request):
    context = {
        'GYEONGPO_score_msg': get_GYEONGPO_score_msg(),
        'GORAEBUL_score_msg': get_GORAEBUL_score_msg(),
        'NAKSAN_score_msg': get_NAKSAN_score_msg(),
        'DAECHON_score_msg': get_DAECHON_score_msg(),
        'MANGSANG_score_msg': get_MANGSANG_score_msg(),
        'SOKCHO_score_msg': get_SOKCHO_score_msg(),
        'SONGJUNG_score_msg': get_SONGJUNG_score_msg(),
        'IMRANG_score_msg': get_IMRANG_score_msg(),
        'JUNGMUN_score_msg': get_JUNGMUN_score_msg(),
        'HAE_score_msg': get_HAE_score_msg(),
        
        'GYEONGPO_lon': get_GYEONGPO_lon(),
        'GORAEBUL_lon': get_GORAEBUL_lon(),
        'NAKSAN_lon': get_NAKSAN_lon(),
        'DAECHON_lon': get_DAECHON_lon(),
        'MANGSANG_lon': get_MANGSANG_lon(),
        'SOKCHO_lon': get_SOKCHO_lon(),
        'SONGJUNG_lon': get_SONGJUNG_lon(),
        'IMRANG_lon': get_IMRANG_lon(),
        'JUNGMUN_lon': get_JUNGMUN_lon(),
        'HAE_lon': get_HAE_lon(),
        
        'GYEONGPO_lat': get_GYEONGPO_lat(),
        'GORAEBUL_lat': get_GORAEBUL_lat(),
        'NAKSAN_lat': get_NAKSAN_lat(),
        'DAECHON_lat': get_DAECHON_lat(),
        'MANGSANG_lat': get_MANGSANG_lat(),
        'SOKCHO_lat': get_SOKCHO_lat(),
        'SONGJUNG_lat': get_SONGJUNG_lat(),
        'IMRANG_lat': get_IMRANG_lat(),
        'JUNGMUN_lat': get_JUNGMUN_lat(),
        'HAE_lat': get_HAE_lat(),

        
    }
    context_json = json.dumps(context)  # JSON 형식의 문자열로 변환
    return render(request, 'control.html', {'contextjson': context_json})


