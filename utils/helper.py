from app.models import CustomUser
from django.core.mail import send_mail


def Employee_id(user_id):
    user = CustomUser.objects.get(id=user_id)
    role = user.role
    if role == "E":
        return True
    return False


def Send_emails(message, recipient, request):
    send_mail(
        subject="Task",
        message=message,
        from_email=request.user,
        recipient_list=[recipient]
    )
