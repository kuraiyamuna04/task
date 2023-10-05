from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.decorators import RequiredManager, RequiredAdmin
from .serializers import TaskSerializers, TaskDetailsSerializer
from utils.helper import Employee_id, Send_emails
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
            s = serializer.save()
            employee_email = s.assigned_to
            Send_emails(assigned,employee_email,request)

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
            task_status = request.data["status"]
            if not Employee_id(user_id) or not task_status:
                return Response(unauthorised, status=status.HTTP_401_UNAUTHORIZED)

            task = TaskModel.objects.get(id=pk, assigned_to=user_id)
            serializer = TaskSerializers(task,
                                         data=request.data,
                                         partial=True)
            serializer.is_valid()
            s = serializer.save()
            if task_status == TaskModel.REVIEW:
                manager_email = s.assigned_by
                Send_emails(review,manager_email,request)
            return Response(serializer.data)
        except Exception:
            return Response(no_data, status=status.HTTP_400_BAD_REQUEST)


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
            s = serializer.save()
            employee_email = s.assigned_to
            Send_emails(updated,employee_email,request)
            return Response(serializer.data)
        except TaskModel.DoesNotExist:
            return Response(no_data, status=status.HTTP_400_BAD_REQUEST)
