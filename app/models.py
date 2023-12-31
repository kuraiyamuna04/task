from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomManager
from phonenumber_field.modelfields import PhoneNumberField
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('', filename)


class CustomUser(AbstractUser):
    Employee = "E"
    Manager = "M"
    Admin = "A"
    ROLES = ((Admin, "admin"),
             (Manager, "manager"),
             (Employee, "employee")
             )
    username = None
    email = models.EmailField(max_length=200, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='E')
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'role']

    objects = CustomManager()

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE,
        primary_key=True, related_name="userProfiles", db_index=True
    )
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    address = models.CharField(max_length=50)
    profile_img = models.ImageField(upload_to=get_file_path)

    class Meta:
        indexes = [
            models.Index(fields=['user'])
        ]

    def __str__(self):
        return self.first_name
