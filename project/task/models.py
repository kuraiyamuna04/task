from django.db import models

from app.models import CustomUser

STATUS = (("TD", "to-do"),
          ("P", "in-progress"),
          ("R", "review"),
          ("C", "complete")
          )


class TaskModel(models.Model):
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
    status = models.CharField(max_length=20, choices=STATUS, default='TD')

    def __str__(self):
        return self.task
