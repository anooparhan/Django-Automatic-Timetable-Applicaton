# Generated by Django 4.2.3 on 2024-10-20 06:06

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_staff_available_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='available_days',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], max_length=40),
        ),
    ]
