from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
class UserManager(BaseUserManager):
    def create_user(self, user_id, user_email, user_password=None, **extra_fields):
        if not user_id:
            raise ValueError('The User ID field must be set')
        if not user_email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(user_email)
        user = self.model(user_id=user_id, user_email=email, **extra_fields)
        user.set_password(user_password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_id, user_email, user_password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(user_id, user_email, user_password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('police', '일반경찰'),
        ('admin', '관리자'),
        ('supervisor', '관제사'),
    )
    user_no = models.AutoField(primary_key=True)  # 회원번호
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='police')  # 권한
    user_phone = models.CharField(max_length=20, blank=False)  # 휴대폰번호
    user_name = models.CharField(max_length=100, blank=False)  # 이름
    user_birth = models.DateField(blank=False)  # 생일
    user_address = models.CharField(max_length=255, blank=False, null=False)  # 주소
    user_detail_address = models.CharField(max_length=255, blank=False, null=False) # 상세 주소
    user_id = models.CharField(max_length=50, unique=True, blank=False)  # 회원 ID
    user_email = models.EmailField(unique=True, blank=False)  # 회원 이메일
    user_joinday = models.DateTimeField(auto_now_add=True, blank=False)  # 회원 가입날짜

    is_active = models.BooleanField(default=True)  # 이메일 인증 등 을 통해 커스텀 가능
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['user_email', 'user_name', 'user_phone', 'user_birth', 'user_address', 'user_detail_address']

    class Meta:
        db_table = 'user'

class Beach(models.Model):
    beach_no = models.AutoField(primary_key=True)  # 해수욕장 번호
    beach_name = models.CharField(max_length=100, blank=False)  # 해수욕장 이름
    beach_region = models.CharField(max_length=100, blank=False)  # 지역
    beach_lat = models.FloatField(null = False,blank=False) # 위도
    beach_lon = models.FloatField(null= False, blank=False) # 경도
    # 아래 3 컬럼은 날씨를 위한 값, null=True (이안류 제공하는 10개 해수욕에 해당하지 않는 값이 있기 때문에)
    beach_widget_id = models.CharField(null = True, max_length=50 ) # widget_id 
    nx = models.IntegerField(null = True)
    ny =  models.IntegerField(null = True)

    class Meta:
        db_table = 'beach'

class Notice_board(models.Model):
    notice_id = models.AutoField(primary_key=True)  # 게시물 고유 번호
    user_no = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, db_column='user_no')  # 회원번호 - user 가 삭제되어도 데이터 남아있도록
    beach_no = models.ForeignKey(Beach, on_delete=models.SET_NULL, db_column='beach_no', null=True, blank=True)
    notice_title = models.CharField(max_length=200, blank=False)  # 제목
    notice_img = models.CharField(max_length=255, blank=True, null=True)  # 이미지
    notice_views = models.IntegerField(default=0)  # 조회수
    notice_wdate = models.DateTimeField(blank=False, default=timezone.now)  # 작성일
    notice_contents = models.TextField(blank=True, null=True)  # 본문

    class Meta:
        db_table = 'notice_board'

class Event_board(models.Model):
    event_id = models.AutoField(primary_key=True)  # 게시물 고유 번호
    user_no = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='user_no', null=True)  # 회원번호
    beach_no = models.ForeignKey(Beach, on_delete=models.SET_NULL, db_column='beach_no',null=True, blank=True)
    event_title = models.CharField(max_length=200, blank=False)  # 제목
    event_img = models.CharField(max_length=255, blank=True, null=True)  # 이미지
    event_views = models.IntegerField(default=0)  # 조회수
    event_wdate = models.DateTimeField( blank=False, default=timezone.now)  # 작성일
    event_contents= models.TextField(blank=True, null=True)  # 본문

    class Meta:
        db_table = 'event_board'

class CCTV(models.Model):
    cctv_code = models.AutoField(primary_key=True)  # CCTV 코드
    beach_no = models.OneToOneField(Beach, on_delete=models.CASCADE, db_column='beach_no')  # 해수욕장 번호
    cctv_location = models.CharField(max_length=255, blank=False)  # 위치
    cctv_url = models.URLField(max_length=255, blank=False)  # 실시간 URL

    class Meta:
        db_table = 'cctv'


# 댓글 일단 보류
# class Comment(models.Model):
#     comment_id = models.CharField(max_length=20, primary_key=True)  # 댓글 고유 번호
#     user_no = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_no')  # 회원번호
#     auth_no = models.ForeignKey(Authority, on_delete=models.CASCADE, db_column='auth_no')  # 권한번호
#     comment = models.TextField(blank=False)  # 댓글

#     class Meta:
#         db_table = 'comment'


# 인덱스, 유형, 시간(시간 포맷?), 상황, 절차(길게), 목표
# csv 파일 업로드 목적 
class Scenario(models.Model):
    scenario_id = models.AutoField(primary_key=True) # 인덱스 
    scenario_code = models.CharField(max_length=20)  # 시나리오 유형
    scenario_time = models.DateTimeField(blank=False, null=False)  #시나리오 발생 시각
    scenario_situation = models.TextField(blank=False, null=False) # 시나리오 상황
    scenario_process = models.TextField(blank=False, null=False)  # 시나리오 절차
    scenario_goals = models.TextField(blank=False, null=False) # 시나리오 목표


    class Meta:
        db_table = 'scenario'




# class ScenarioEval(models.Model):
#     scenario_code = models.ForeignKey(Scenario, on_delete=models.CASCADE, db_column='scenario_code')  # 시나리오 코드
#     category = models.CharField(max_length=100, blank=False)  # 유형
#     time = models.DateTimeField(blank=False)  # 시간
#     story = models.TextField(blank=False)  # 상황
#     goal = models.TextField(blank=False)  # 목표

#     class Meta:
#         db_table = 'scenario_eval'