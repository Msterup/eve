# Generated by Django 5.1 on 2024-08-22 18:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battlefield_tracker', '0005_livebattlefield_scheduledbattlefield_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledbattlefield',
            name='is_between_noon_and_four_hours_after',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='livebattlefield',
            name='fc',
            field=models.CharField(default='No planned FC', max_length=10),
        ),
        migrations.AlterField(
            model_name='scheduledbattlefield',
            name='expected_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 22, 22, 31, 49, 797382, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='scheduledbattlefield',
            name='fc',
            field=models.CharField(default='No planned FC', max_length=10),
        ),
    ]
