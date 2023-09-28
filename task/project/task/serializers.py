from rest_framework import serializers
from .models import TaskModel


class TaskSerializers(serializers.ModelSerializer):

    class Meta:
        model = TaskModel
        fields = "__all__"


class TaskDetailsSerializer(serializers.ModelSerializer):
    assignee = serializers.SerializerMethodField()
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = TaskModel
        fields = ("task", "assignee","reporter")

    def get_assignee(self, obj):
        user = {
            "first_name": obj.assigned_by.userProfiles.first_name,
            "email": obj.assigned_by.email,
            "profile_img": obj.assigned_by.userProfiles.profile_img
        }
        return user

    def get_reporter(self, obj):
        user = {
            "first_name": obj.assigned_to.userProfiles.first_name,
            "email": obj.assigned_to.email,
            "profile_img": obj.assigned_to.userProfiles.profile_img
        }
        return user
