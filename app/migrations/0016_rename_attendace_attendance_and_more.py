# Generated by Django 4.1.7 on 2023-05-15 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_attendace_attendace_report'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Attendace',
            new_name='Attendance',
        ),
        migrations.RenameModel(
            old_name='Attendace_Report',
            new_name='Attendance_Report',
        ),
    ]
