# Generated by Django 3.2.23 on 2024-02-06 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_delete_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
