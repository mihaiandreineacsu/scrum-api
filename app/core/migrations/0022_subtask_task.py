# Generated by Django 3.2.18 on 2023-04-23 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_category_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.task'),
        ),
    ]
