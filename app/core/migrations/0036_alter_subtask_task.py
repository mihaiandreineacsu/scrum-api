# Generated by Django 3.2.18 on 2023-05-29 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20230529_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='core.task'),
        ),
    ]
