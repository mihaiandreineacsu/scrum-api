# Generated by Django 3.2.25 on 2024-04-29 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20240429_1107'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='contact',
            name='unique_user_email',
        ),
        migrations.RemoveConstraint(
            model_name='contact',
            name='unique_user_phone',
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(condition=models.Q(('email__isnull', False), ('email__exact', '')), fields=('user', 'email'), name='unique_user_email'),
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(condition=models.Q(('phone_number__isnull', False), ('phone_number__exact', '')), fields=('user', 'phone_number'), name='unique_user_phone'),
        ),
    ]