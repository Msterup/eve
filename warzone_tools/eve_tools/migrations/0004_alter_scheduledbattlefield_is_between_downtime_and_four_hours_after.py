# Generated by Django 5.1 on 2024-08-31 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eve_tools', '0003_alter_solarsystem_contested_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledbattlefield',
            name='is_between_downtime_and_four_hours_after',
            field=models.BooleanField(default=False),
        ),
    ]
