# Generated by Django 4.2.4 on 2023-10-31 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_staff"),
    ]

    operations = [
        migrations.RenameField(
            model_name="student",
            old_name="session_year",
            new_name="session_year_id",
        ),
    ]
