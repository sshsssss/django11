# Generated by Django 5.0.3 on 2024-06-21 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_question_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='exam_type',
            new_name='frame_text_content_id',
        ),
        migrations.RenameField(
            model_name='exam',
            old_name='level',
            new_name='grade_level',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='difficulty',
            new_name='difficult',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='create_user',
        ),
        migrations.AddField(
            model_name='exam',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='exam',
            name='limit_end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='limit_start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='paper_type',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]
