# gunicorn.conf.py

import os
import sys
import threading
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
application = get_wsgi_application()

def start_scheduler():
    from control.scheduler import start
    start()

def post_fork(server, worker):
    if 'runserver' in sys.argv or 'uwsgi' in sys.argv or 'gunicorn' in sys.argv:
        threading.Thread(target=start_scheduler).start()
