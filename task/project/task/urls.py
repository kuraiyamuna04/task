from django.urls import path
from . import views

urlpatterns = [
    path('create-task', views.ManagerAccessView.as_view(), name="create-task"),
    path('updateapi-admin',views.AdminAccessView.as_view, name="updateapi-admin"),
    path('view-task',views.EmployeeAccessView.as_view, name="view-task")
]
