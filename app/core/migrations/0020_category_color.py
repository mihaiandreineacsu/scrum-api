# Generated by Django 3.2.18 on 2023-04-20 17:06

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None),
        ),
    ]
