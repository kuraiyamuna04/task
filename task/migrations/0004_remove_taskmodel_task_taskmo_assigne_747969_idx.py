# Generated by Django 4.2.5 on 2023-10-10 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_taskmodel_task_taskmo_assigne_747969_idx'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='taskmodel',
            name='task_taskmo_assigne_747969_idx',
        ),
    ]
