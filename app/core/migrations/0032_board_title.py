# Generated by Django 3.2.18 on 2023-05-14 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20230514_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='title',
            field=models.CharField(default='Untitled', max_length=255),
        ),
    ]
