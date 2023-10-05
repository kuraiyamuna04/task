from django.db import models

from app.models import CustomUser


class TaskModel(models.Model):
    TODO = "TD"
    IN_PROGRESS = "P"
    REVIEW = "R"
    COMPLETE = "C"
    STATUS = ((TODO, "todo"),
              (IN_PROGRESS, "in-progress"),
              (REVIEW, "review"),
              (COMPLETE, "complete")
              )

    task = models.CharField(max_length=500)
    due_date = models.DateField()
    assigned_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT,
        related_name="assigned_by"
    )
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT,
        related_name="assigned_to"
    )

    status = models.CharField(max_length=20, choices=STATUS, default="TD")

    def __str__(self):
        return self.task
