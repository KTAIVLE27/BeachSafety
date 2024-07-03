# from django.shortcuts import render
# from django.contrib.auth.models import User
# from main.models import User  # Ensure this is the correct import
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from main.models import User
from main.models import Event_board, Notice_board
import json
from main.forms import *
import logging

def admin_home(request):
    return render(request, 'adminpanel/admin_home.html')

def senario(request):
    return render(request, 'adminpanel/senario.html')

def board_manage(request):
    posts = Event_board.objects.all()
    return render(request, 'adminpanel/board_manage.html', {'posts': posts})

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
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'adminpanel/user_list.html', context)
  
def notice_manage(request):
    posts = Notice_board.objects.all()
    return render(request, 'adminpanel/notice_manage.html', {'posts':posts})

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


logger = logging.getLogger(__name__)
@login_required
def create_notice(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user_no = request.user
            notice.notice_wdate = timezone.now()
            notice.save()
            return redirect('adminpanel:notice_manage')
    else:
        form = PostForm()
    beaches = Beach.objects.all()
    return render(request, 'adminpanel/create_notice.html', {'beaches': beaches})