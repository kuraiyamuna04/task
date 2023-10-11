from rest_framework import serializers

from .models import TaskModel
from app.models import CustomUser, UserProfile
from app.serializerls import UserProfileSerializer, UserSerializer


class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = "__all__"



class UpdateTaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ("status", "time_needed")


class TaskDetailsSerializer(serializers.ModelSerializer):
    assignee = serializers.SerializerMethodField()
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = TaskModel
        fields = ("id", "task", "assignee", "reporter", "status", "rate_per_hour", "time_needed")

    def get_assignee(self, obj):
        obj = obj.assigned_by.userProfiles
        serializer = UserProfileSerializer(
            obj, context={"request": self.context['request']}
        )
        return serializer.data

    #
    def get_reporter(self, obj):
        obj = obj.assigned_to.userProfiles
        serializer = UserProfileSerializer(
            obj, context={"request": self.context['request']}
        )
        return serializer.data
