# Generated by Django 3.2.16 on 2023-01-07 17:46

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_task_sub_tasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='sub_tasks',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, max_length=255), blank=True, default=list, size=None),
        ),
    ]
