from django.db import models

from app.models import CustomUser


class TaskModel(models.Model):
    task = models.CharField(max_length=500)
    due_date = models.DateField()
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=None, related_name="assigned_by")
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="assigned_to")

    def __str__(self):
        return self.task
