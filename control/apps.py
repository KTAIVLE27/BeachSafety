from django.apps import AppConfig
import sys

class ControlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "control"
    
    def ready(self):
        pass  # 더 이상 여기서 스케줄러를 시작하지 않음
