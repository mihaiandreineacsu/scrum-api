# Generated by Django 3.2.25 on 2024-04-21 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_auto_20240421_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(default='anonymous', max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]