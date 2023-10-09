from django.urls import path
from . import views

urlpatterns = [
    path('create-task', views.ManagerAccessView.as_view(), name="create-task"),
    path('updatetask-admin/<str:pk>', views.UpdateTaskView.as_view(), name="updateapi-admin"),
    path('view-task', views.EmployeeAccessView.as_view(), name="view-task"),
    path("admin-access", views.AdminAccessView.as_view(), name="admin_access"),
    path("update-status/<str:pk>", views.UpdateStatusView.as_view(), name="update-status"),
    path("generate_salary/<str:pk>", views.GenerateSalary.as_view(), name="earnings")
]
