# Generated by Django 5.1 on 2024-10-10 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='time_limit',
        ),
    ]
