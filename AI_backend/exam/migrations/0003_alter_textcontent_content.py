# Generated by Django 5.0.3 on 2024-06-21 06:47

import jsonfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_question_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textcontent',
            name='content',
            field=jsonfield.fields.JSONField(),
        ),
    ]
