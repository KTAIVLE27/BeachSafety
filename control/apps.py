from django.apps import AppConfig
import sys

class ControlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "control"
    
    def ready(self):
        pass  
