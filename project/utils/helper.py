from app.models import CustomUser


def Employee_id(user_id):
    user = CustomUser.objects.get(id=user_id)
    role = user.role
    if role == "E":
        return True
    return False




