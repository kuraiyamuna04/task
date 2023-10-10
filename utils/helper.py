import datetime
from project.settings import EMAIL_HOST_USER
from app.models import CustomUser
from django.core.mail import send_mail

from task.models import TaskModel


def employee_id(user_id):
    try:
        _ = CustomUser.objects.get(id=user_id, role="E")
        return True
    except:
        return False


def send_emails(message, recipient):
    send_mail(
        subject="Task",
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[recipient]
    )


def calculate_earning(task):
    time = task.time_needed
    rate = task.rate_per_hour
    total_earning = time * rate
    return total_earning


def my_scheduled_task():
    current_time = datetime.date.today() + datetime.timedelta(days=1)
    tasks = TaskModel.objects.filter(due_date=current_time)
    for task in tasks:
        send_emails(
            message=f"tomorrow is the last date of submitting your task {task.task}",
            recipient=task.assigned_to
        )
