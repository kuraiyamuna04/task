from django.urls import path
from . import views

urlpatterns = [
    path('create-task', views.CreateTaskView.as_view(), name="create-task")
]
