# Generated by Django 5.0.6 on 2024-07-15 14:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='hesapTarih',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
