# Generated by Django 5.0.6 on 2024-07-19 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_question_choice_userresponse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='selected_choice',
        ),
        migrations.RemoveField(
            model_name='question',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='question',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='user',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='UserResponse',
        ),
    ]