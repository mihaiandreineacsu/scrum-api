# Generated by Django 3.2.25 on 2024-04-29 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_remove_contact_unique_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(blank=True, default='Anonymous', max_length=255, null=True),
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(condition=models.Q(('phone_number__isnull', False)), fields=('user', 'phone_number'), name='unique_user_phone'),
        ),
    ]
