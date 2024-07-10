from django.apps import AppConfig


class ControlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "control"
    
    def ready(self):
        from . import scheduler
        scheduler.start()
