# Generated by Django 3.2.18 on 2023-06-05 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_alter_subtask_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
