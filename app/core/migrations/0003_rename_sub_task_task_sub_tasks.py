# Generated by Django 3.2.15 on 2022-09-16 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='sub_task',
            new_name='sub_tasks',
        ),
    ]
