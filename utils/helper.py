from app.models import CustomUser
from django.core.mail import send_mail


def employee_id(user_id):
    try:
        _ = CustomUser.objects.get(id=user_id, role="E")
        return True
    except:
        return False


def send_emails(message, recipient, request):
    send_mail(
        subject="Task",
        message=message,
        from_email=request.user,
        recipient_list=[recipient]
    )


def calculate_earning(task):
    time = task.time_needed
    rate = task.rate_per_hour
    total_earning = time * rate
    return total_earning
