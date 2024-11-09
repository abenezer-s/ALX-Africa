# Generated by Django 5.1 on 2024-10-08 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('program', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivation_letter', models.TextField(max_length=600)),
                ('submitted_at', models.DateField()),
                ('state', models.CharField(choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], default=None, max_length=20)),
                ('course', models.ManyToManyField(default=None, to='course.course')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learner', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='program_course_owner', to=settings.AUTH_USER_MODEL)),
                ('program', models.ManyToManyField(default=None, to='program.program')),
            ],
        ),
    ]