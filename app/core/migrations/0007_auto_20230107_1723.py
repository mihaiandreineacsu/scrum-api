# Generated by Django 3.2.16 on 2023-01-07 17:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_user_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='link',
        ),
        migrations.AlterField(
            model_name='task',
            name='sub_tasks',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), blank=True, size=None),
        ),
    ]
