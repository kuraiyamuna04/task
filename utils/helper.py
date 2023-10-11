import datetime
from project.settings import EMAIL_HOST_USER
from app.models import CustomUser
from django.core.mail import send_mail
from django.db.models import Q
from tabulate import tabulate

from task.models import TaskModel


def employee_id(user_id):
    try:
        _ = CustomUser.objects.get(id=user_id, role=CustomUser.Employee)
        return True
    except:
        return False


def send_emails(subject, message, recipient):
    send_mail(
        subject=subject,
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


def create_table(header,data):
    table = tabulate(data, headers=header, tablefmt="grid")
    return table