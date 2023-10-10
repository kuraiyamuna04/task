from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.decorators import RequiredManager, RequiredAdmin
from .serializers import TaskSerializers, TaskDetailsSerializer, UpdateTaskSerializers
from utils.helper import employee_id, send_emails, calculate_earning
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
            if not employee_id(assigned_id):
                return Response(
                    unauthorised, status=status.HTTP_401_UNAUTHORIZED
                )
            serializer.initial_data["assigned_by"] = request.user.id
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            task = serializer.save()
            employee_email = task.assigned_to
            send_emails(assigned, employee_email)

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
            if not employee_id(user_id):
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
            if not employee_id(user_id) or task_status == TaskModel.COMPLETE:
                return Response(unauthorised, status=status.HTTP_401_UNAUTHORIZED)

            task = TaskModel.objects.get(id=pk, assigned_to=user_id)
            serializer = UpdateTaskSerializers(task,
                                               data=request.data,
                                               partial=True)
            serializer.is_valid()
            task = serializer.save()
            if task_status == TaskModel.REVIEW:
                manager_email = task.assigned_by
                send_emails(review, manager_email)
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
            task = serializer.save()
            employee_email = task.assigned_to
            send_emails(updated, employee_email)
            return Response(serializer.data)
        except TaskModel.DoesNotExist:
            return Response(no_data, status=status.HTTP_400_BAD_REQUEST)


class GenerateSalary(APIView):
    permission_classes = [IsAuthenticated, RequiredManager]

    def get(self, request, pk):

        try:
            all_task = TaskModel.objects.filter(assigned_to=pk)
            complete_task = all_task.filter(status=TaskModel.COMPLETE).count()
            if all_task.count() == complete_task:
                count = 0
                for task in all_task:
                    count = count + calculate_earning(task)
                send_emails(
                    message=f"Hi your total salary for all tasks is Rs. {count}",
                    recipient=task.assigned_to,
                    request=request
                )
                return Response({"total salary is ": count})

            return Response({"msg": "All tasks are not completed by this employee"})

        except TaskModel.DoesNotExist:
            return Response(no_data, status.HTTP_400_BAD_REQUEST)
