# Generated by Django 5.1 on 2024-10-08 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('number_of_modules', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('created_at', models.DateField()),
                ('duration', models.IntegerField(default=None)),
                ('complete_within', models.DecimalField(decimal_places=0, default=None, max_digits=2)),
                ('category', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.category')),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='course_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
