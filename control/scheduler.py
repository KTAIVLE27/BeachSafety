# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from .utils import *

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # 10초마다 실행되는 작업 추가
    scheduler.add_job(
        fetch_rip_current_data,
        trigger=IntervalTrigger(seconds=300), #5분에 한번씩
        id='fetch_rip_current_data_job',  # 작업 ID
        name='fetch rip current data Job',  # 작업 이름
        replace_existing=True,
    )
    # # 10초마다 실행되는 두 번째 작업 추가
    # scheduler.add_job(
    #     get_beach_score_msg,
    #     trigger=IntervalTrigger(seconds=10),
    #     id='get_beach_score_msg_job',  # 작업 ID
    #     name='get beach score msg Job',  # 작업 이름
    #     replace_existing=True,
    # )
    
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started!")
