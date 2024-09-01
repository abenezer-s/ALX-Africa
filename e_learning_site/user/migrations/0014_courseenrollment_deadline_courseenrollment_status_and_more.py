# Generated by Django 5.1 on 2024-08-31 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_courseenrollment_number_of_modules_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseenrollment',
            name='deadline',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='courseenrollment',
            name='status',
            field=models.CharField(choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('in complete', 'In Complete')], default='in porgress', max_length=11),
        ),
        migrations.AddField(
            model_name='programenrollment',
            name='deadline',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='programenrollment',
            name='status',
            field=models.CharField(choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('in complete', 'In Complete')], default='in porgress', max_length=11),
        ),
    ]
