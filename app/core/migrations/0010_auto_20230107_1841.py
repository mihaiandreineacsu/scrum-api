# Generated by Django 3.2.16 on 2023-01-07 18:41

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_task_sub_tasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assignees',
            field=models.ManyToManyField(blank=True, default=list, related_name='assignee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='sub_tasks',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(max_length=255), blank=True, default=list, size=None),
        ),
    ]
