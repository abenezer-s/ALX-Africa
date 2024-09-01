# Generated by Django 5.1 on 2024-08-30 17:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0011_module_completed_module_completed_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='module',
            name='completed_at',
        ),
        migrations.CreateModel(
            name='LearnerCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateField()),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='content.course')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='content.module')),
                ('program', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='content.program')),
            ],
        ),
    ]
