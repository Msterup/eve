# Generated by Django 5.1 on 2024-08-23 16:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battlefield_tracker', '0006_scheduledbattlefield_battlefield_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledbattlefield',
            name='expected_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 23, 20, 8, 9, 535844, tzinfo=datetime.timezone.utc)),
        ),
    ]
