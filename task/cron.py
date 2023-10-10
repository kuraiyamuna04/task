from utils.helper import my_scheduled_task
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_scheduled_task, 'interval', hours=1)
    scheduler.start()
