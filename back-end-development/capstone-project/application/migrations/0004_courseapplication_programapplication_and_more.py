# Generated by Django 5.1 on 2024-10-22 09:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_alter_application_course_alter_application_program'),
        ('course', '0006_rename_decription_course_description'),
        ('program', '0003_program_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivation_letter', models.TextField(max_length=600)),
                ('submitted_at', models.DateField()),
                ('state', models.CharField(choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], default=None, max_length=20)),
                ('course', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_course', to='course.course')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_learner', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='application_course_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivation_letter', models.TextField(max_length=600)),
                ('submitted_at', models.DateField()),
                ('state', models.CharField(choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], default=None, max_length=20)),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prog_learner', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='application_program_owner', to=settings.AUTH_USER_MODEL)),
                ('program', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_program', to='program.program')),
            ],
        ),
        migrations.DeleteModel(
            name='Application',
        ),
    ]