from django.db import models

class Authority(models.Model):
    auth_no = models.AutoField(primary_key=True)  # 권한 번호
    auth_name = models.CharField(max_length=100, blank=False, unique=True)  # 권한 이름

    class Meta:
        #managed = False
        db_table = 'authority'


class User(models.Model):
    user_no = models.AutoField(db_column='user_no', primary_key=True)  # 회원번호
    auth_no = models.OneToOneField(Authority, on_delete=models.CASCADE, db_column='auth_no')  # 권한번호
    user_password = models.CharField(max_length=128, blank=False)  # 비밀번호
    user_phone = models.CharField(max_length=20, blank=False)  # 휴대폰번호
    user_name = models.CharField(max_length=100, blank=False)  # 이름
    user_birth = models.DateField(blank=False)  # 생일
    user_address = models.CharField(max_length=255, blank=True, null=True)  # 주소
    user_id = models.CharField(max_length=50, unique=True, blank=False)  # 회원 ID
    user_email = models.EmailField(unique=True, blank=False)  # 회원 이메일
    user_joinday = models.DateTimeField(auto_now_add=True, blank=False)  # 회원 가입날짜

    class Meta:
        #managed = False
        db_table = 'user'

class Beach(models.Model):
    beach_no = models.AutoField(max_length=20, primary_key=True)  # 해수욕장 번호
    beach_name = models.CharField(max_length=100, blank=False)  # 해수욕장 이름
    beach_region = models.CharField(max_length=100, blank=False)  # 지역

    class Meta:
        #managed = False
        db_table = 'beach'

class Notice_board(models.Model):
    board_id = models.CharField(max_length=20, primary_key=True)  # 게시물 고유 번호
    user_no = models.ForeignKey(User, on_delete=models.RESTRICT,db_column='user_no')  # 회원번호
    #auth_no = models.OneToOneField(Authority, db_column='auth_no')  # 권한번호
    beach_no = models.ForeignKey(Beach,on_delete=models.RESTRICT, db_column='beach_no')
    notice_title = models.CharField(max_length=200, blank=False)  # 제목
    notice_writer = models.CharField(max_length=100, blank=False)  # 작성자
    notice_img = models.CharField(max_length=255, blank=True, null=True)  # 이미지
    notice_hit = models.IntegerField(default=0)  # 조회수
    notice_rdate = models.DateField(blank=True, null=True)  # 작성일
    notice_ield = models.TextField(blank=True, null=True)  # 본문

    class Meta:
        #managed = False
        db_table = 'notice_board'

class Event_board(models.Model):
    board_id = models.CharField(max_length=20, primary_key=True)  # 게시물 고유 번호
    user_no = models.ForeignKey(User,on_delete=models.RESTRICT, db_column='user_no')  # 회원번호
    #auth_no = models.ForeignKey(Authority, db_column='auth_no')  # 권한번호
    beach_no = models.ForeignKey(Beach,on_delete=models.RESTRICT, db_column='beach_no')
    event_title = models.CharField(max_length=200, blank=False)  # 제목
    event_writer = models.CharField(max_length=100, blank=False)  # 작성자
    event_img = models.CharField(max_length=255, blank=True, null=True)  # 이미지
    event_hit = models.IntegerField(default=0)  # 조회수
    event_rdate = models.DateField(blank=True, null=True)  # 작성일
    event_ield = models.TextField(blank=True, null=True)  # 본문

    class Meta:
        #managed = False
        db_table = 'event_board'



# 댓글 일단 보류
# class Comment(models.Model):
#     comment_id = models.CharField(max_length=20, primary_key=True)  # 댓글 고유 번호
#     user_no = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_no')  # 회원번호
#     auth_no = models.ForeignKey(Authority, on_delete=models.CASCADE, db_column='auth_no')  # 권한번호
#     comment = models.TextField(blank=False)  # 댓글

#     class Meta:
#         db_table = 'comment'


# 다음에 생각 ㅋㅋㅋㅋㅋㅋ
# class Scenario(models.Model):
#     scenario_code = models.CharField(max_length=20, primary_key=True)  # 시나리오 코드
#     scenario_process = models.TextField(blank=False)  # 시나리오 본문
#     scenario_category = models.CharField(max_length=100, blank=False)  # 분류

#     class Meta:
#         db_table = 'scenario'




# class ScenarioEval(models.Model):
#     scenario_code = models.ForeignKey(Scenario, on_delete=models.CASCADE, db_column='scenario_code')  # 시나리오 코드
#     category = models.CharField(max_length=100, blank=False)  # 유형
#     time = models.DateTimeField(blank=False)  # 시간
#     story = models.TextField(blank=False)  # 상황
#     goal = models.TextField(blank=False)  # 목표

#     class Meta:
#         db_table = 'scenario_eval'









class CCTV(models.Model):
    cctv_code = models.AutoField(primary_key=True)  # CCTV 코드
    beach_no = models.OneToOneField(Beach, on_delete=models.CASCADE, db_column='beach_no')  # 해수욕장 번호
    cctv_location = models.CharField(max_length=255, blank=False)  # 위치
    cctv_url = models.URLField(max_length=255, blank=False)  # 실시간 URL

    class Meta:
        #managed = False
        db_table = 'cctv'




class RipApi(models.Model):
    beach_code = models.CharField(max_length=20, primary_key=True)  # 해안 코드
    beach_no = models.OneToOneField(Beach, on_delete=models.CASCADE, db_column='beach_no')  # 해수욕장 번호
    date_type = models.CharField(max_length=10, blank=False)  # 데이터 종류
    date = models.DateTimeField(blank=False)  # 날짜
    result_type = models.CharField(max_length=10, blank=False)  # 결과 타입 (json, xml 등)

    class Meta:
        #managed = False
        db_table = 'rip_api'

