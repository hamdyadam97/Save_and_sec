# Generated by Django 5.2.1 on 2025-06-03 18:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_section_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='residency_end_date',
            field=models.DateField(default=datetime.date(2025, 12, 31)),
        ),
    ]
