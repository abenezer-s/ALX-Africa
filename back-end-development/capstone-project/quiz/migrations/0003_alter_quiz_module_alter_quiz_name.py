# Generated by Django 5.1 on 2024-10-13 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0003_media_name_alter_module_course_alter_module_name'),
        ('quiz', '0002_quiz_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='module',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='module_quiz', to='module.module'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(default='default test name', max_length=30, unique=True),
        ),
    ]