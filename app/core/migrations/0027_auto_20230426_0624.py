# Generated by Django 3.2.18 on 2023-04-26 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_subtask_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtask',
            name='task',
        ),
        migrations.AddField(
            model_name='task',
            name='subtasks',
            field=models.ManyToManyField(blank=True, default=list, related_name='assignee', to='core.Subtask'),
        ),
    ]