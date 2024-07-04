from django.apps import AppConfig


# 관리자 자동 생성을 위한 설정
class mainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'main'  # 앱의 실제 이름을 입력하세요. 

    
    def ready(self):
        import main.signals  # 시그널을 임포트합니다.
