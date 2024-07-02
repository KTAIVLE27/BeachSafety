from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.


# views.py
# from .utils import get_variable_a, get_variable_meta
# import json
# def control_view(request):
#     context = {
#         'latest_data': get_variable_a(),
#         'meta': get_variable_meta(),
        
#     }
#     return render(request, 'control.html', context)






from .utils import *
import json
def control_view(request):
    context = {
        'score_msg': get_variable_score_msg(),
        'meta': get_variable_meta(),
        'lon': get_variable_lon(),
        'lat':get_variable_lat(),
        
    }
    context_json = json.dumps(context)  # JSON 형식의 문자열로 변환
    return render(request, 'control.html', {'contextjson': context_json})


