from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app.models import CustomUser, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True},
                        'confirm_password': {'write_only': True}
                        }
        fields = '__all__'

    def save(self, **kwargs):
        if self.validated_data["password"] != self.validated_data["confirm_password"]:
            raise ValueError("Password and Confirm_password must be same")
        self.validated_data["password"] = make_password(self.validated_data["password"])
        self.validated_data["confirm_password"] = make_password(self.validated_data["confirm_password"])
        self.validated_data["is_active"] = True
        super(UserSerializer, self).save(**kwargs)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("phone_number", "password")


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"
