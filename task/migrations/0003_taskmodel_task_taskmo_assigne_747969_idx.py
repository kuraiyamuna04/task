# Generated by Django 4.2.5 on 2023-10-10 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_taskmodel_rate_per_hour_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='taskmodel',
            index=models.Index(fields=['assigned_to'], name='task_taskmo_assigne_747969_idx'),
        ),
    ]
