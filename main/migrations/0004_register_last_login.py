# Generated by Django 5.0.6 on 2024-07-18 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userlogin'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
