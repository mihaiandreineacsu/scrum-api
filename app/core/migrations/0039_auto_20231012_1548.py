# Generated by Django 3.2.18 on 2023-10-12 15:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_alter_task_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='summary',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
