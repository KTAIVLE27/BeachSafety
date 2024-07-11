from django.apps import AppConfig
import sys

class ControlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "control"
    
    def ready(self):
        # 서버가 실행 중일 때만 스케줄러를 시작합니다.
        if 'runserver' in sys.argv or 'uwsgi' in sys.argv or 'gunicorn' in sys.argv:
            from . import scheduler
            scheduler.start()
