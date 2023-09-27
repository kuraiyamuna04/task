from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import UserProfile, CustomUser
from utils.decorators import RequiredManager, RequiredAdmin
from .serializers import TaskSerializers
from utils.helper import Employee_id
from .models import TaskModel


class ManagerAccessView(APIView):
    permission_classes = [IsAuthenticated, RequiredManager]

    def post(self, request):
        serializer = TaskSerializers(data=request.data)
        try:
            assigned_id = request.data["assigned_to"]
            if not Employee_id(assigned_id):
                return Response(
                    {"msg": "You Don't Have Permission To Add This"}, status=status.HTTP_401_UNAUTHORIZED
                )
            user_id = request.user.id
            serializer.initial_data["assigned_by"] = user_id
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        except Exception:
            return Response({"msg:You entered wrong data"}, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user.id
        task = TaskModel.objects.filter(assigned_by=user)
        serializer = TaskSerializers(task, many=True)
        return Response(serializer.data)


class UpdateTaskView(UpdateAPIView):
    permission_classes = [IsAuthenticated, RequiredManager]

    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializers


class AdminAccessView(ListAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticated, RequiredAdmin]

    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializers


class EmployeeAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.role
        task = TaskModel.objects.filter(assigned_to=user)
        serializer = TaskSerializers(task, many=True)
        return Response(serializer.data)
