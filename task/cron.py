from apscheduler.schedulers.background import BackgroundScheduler
from task.schedular import my_scheduled_task


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_scheduled_task, 'interval', hours=1)
    scheduler.start()
