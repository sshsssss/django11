# Generated by Django 5.0.3 on 2024-04-25 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0021_fileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='chapter_intro',
            field=models.CharField(default='test intro', max_length=500, verbose_name='章节简介'),
            preserve_default=False,
        ),
    ]
