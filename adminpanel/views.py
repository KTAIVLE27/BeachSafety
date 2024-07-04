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
from main.models import User
from main.models import Event_board, Notice_board
from django.contrib import messages
import json
from main.forms import *

def admin_home(request):
    return render(request, 'adminpanel/admin_home.html')

def senario(request):
    return render(request, 'adminpanel/senario.html')

def board_manage(request):
    posts = Event_board.objects.all().order_by('-event_wdate')
    
    # 페이징 처리
    paginator = Paginator(posts, 10)  # 페이지당 10개의 게시물
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'adminpanel/board_manage.html', {'posts': posts, 'page_obj': page_obj})

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


def notice_manage(request):
    #posts = Notice_board.objects.prefetch_related('beach_no').all()
    beach_no = request.GET.get('beach_no')
    
    if beach_no == 'common':
        posts = Notice_board.objects.filter(beach_no__isnull=True).order_by('-notice_wdate')
    elif beach_no:
        posts = Notice_board.objects.filter(beach_no=beach_no).order_by('-notice_wdate')
    else:
        posts = Notice_board.objects.all().order_by('-notice_wdate')
    
    
    # 페이징 처리
    paginator = Paginator(posts, 10)  # 페이지당 10개의 게시물
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    beaches = Beach.objects.all()
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