from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from datetime import date
from .models import User  # 커스텀 유저 모델 임포트

#시그널이 여러 번 호출되는 것을 방지하기 위해 플래그를 사용하여 처음 실행될 때만 코드가 수행되도록 함.
user_created = False

@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    #print("Post migrate signal received from:", sender)  # 어떤 앱에서 시그널이 발생했는지 확인
    global user_created
    if not user_created:
        if not User.objects.filter(user_id='admin').exists():
            if not User.objects.filter(user_email='admin@aivle.com').exists():
                User.objects.create_user(
                    user_id='admin',
                    user_email='admin@aivle.com',
                    user_name='김관리',
                    user_phone='010-0000-0000',
                    user_birth=date(1990, 1, 1),
                    user_address='광주 광역시 북구',
                    user_detail_address='KT 신안 본사',
                    user_role='admin',
                    password='aivle202405!'
            )
            print("Admin user created.")
            user_created = True
        else:
            print("Admin user already exists.")
            user_created = True

