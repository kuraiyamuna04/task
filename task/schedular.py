import datetime
from django.db.models import Q
from task.models import TaskModel
from utils.helper import send_emails


def my_scheduled_task():
    current_time = datetime.date.today() + datetime.timedelta(days=1)
    tasks = TaskModel.objects.filter(due_date=current_time)
    tasks = tasks.filter(~Q(status=TaskModel.COMPLETE))
    lst = [
        send_emails
            (
            subject="Last Date of Submission",
            message=f"Tomorrow is the last date of submitting your task {task.task}",
            recipient=task.assigned_to
        )
        for task in tasks
    ]
    return lst
