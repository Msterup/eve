# Generated by Django 5.1 on 2024-09-06 12:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eve_tools', '0003_alter_solarsystem_contested_amount_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledbattlefield',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='battlefields_as_participant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='scheduledbattlefield',
            name='fc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='battlefields_as_fc', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='scheduledbattlefield',
            name='is_between_downtime_and_four_hours_after',
            field=models.BooleanField(default=False),
        ),
    ]
