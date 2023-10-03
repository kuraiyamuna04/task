from rest_framework import status
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from app.models import CustomUser
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.decorators import RequiredManager, RequiredAdmin
from .serializers import TaskSerializers, TaskDetailsSerializer
from utils.helper import Employee_id
from .models import TaskModel
from utils.msg import *


class ManagerAccessView(APIView):
    permission_classes = [IsAuthenticated, RequiredManager]

    def post(self, request):
        serializer = TaskSerializers(
            data=request.data,
            context={'request': self.request}
        )
        try:
            assigned_id = request.data["assigned_to"]
            if not Employee_id(assigned_id):
                return Response(
                    unauthorised, status=status.HTTP_401_UNAUTHORIZED
            )
            serializer.initial_data["assigned_by"] = request.user.id
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            employee_email = CustomUser.objects.get(id=serializer.data["assigned_to"])
            send_mail(
                subject=subject,
                message="You got a task from the manager",
                from_email=request.user,
                recipient_list=[employee_email]
            )

            return Response(serializer.data)

        except Exception:
            return Response(wrong_data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            user = request.user.id
            task = TaskModel.objects.filter(assigned_by=user)
            serializer = TaskDetailsSerializer(
                task, many=True, context={"request": request}
            )
            return Response(serializer.data)
        except TaskModel.DoesNotExist:
            return Response(no_data, status=status.HTTP_400_BAD_REQUEST)


class AdminAccessView(ListAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticated, RequiredAdmin]

    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializers


class EmployeeAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = request.user.id
            if not Employee_id(user_id):
                return Response(unauthorised, status=status.HTTP_401_UNAUTHORIZED)
            task = TaskModel.objects.filter(assigned_to=user_id)
            serializer = TaskDetailsSerializer(
                task, many=True, context={"request": request}
            )
            return Response(serializer.data)
        except Exception:
            return Response(no_data, status=status.HTTP_400_BAD_REQUEST)


class UpdateStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            user_id = request.user.id
            status = request.data["status"]
            if not Employee_id(user_id) or not status:
                return Response(unauthorised, status=status.HTTP_401_UNAUTHORIZED)

            task = TaskModel.objects.get(id=pk)
            serializer = TaskSerializers(task,
                                         data=request.data,
                                         partial=True)
            if task.assigned_to.id == user_id:
                serializer.is_valid()
                serializer.save()
                if status == "R":
                    manager_email = CustomUser.objects.get(id=serializer.data["assigned_by"])
                    send_mail(
                        subject=subject,
                        message="Task is Ready to Review",
                        from_email=request.user,
                        recipient_list=[manager_email]
                    )
                return Response(serializer.data)
        except Exception:
            return Response(no_data, status.HTTP_400_BAD_REQUEST)


class UpdateTaskView(APIView):
    permission_classes = [IsAuthenticated, RequiredManager | RequiredAdmin]

    def patch(self, request, pk):
        try:
            task = TaskModel.objects.get(id=pk)
            serializer = TaskSerializers(task, data=request.data,
                                         partial=True,
                                         context={'request': request}
                                         )
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            employee_email = CustomUser.objects.get(id=serializer.data["assigned_to"])
            send_mail(
                subject=subject,
                message="You Task got Updated",
                from_email=request.user,
                recipient_list=[employee_email]
            )
            return Response(serializer.data)
        except TaskModel.DoesNotExist:
            return Response(no_data, status=status.HTTP_400_BAD_REQUEST)
