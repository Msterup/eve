# Generated by Django 5.1 on 2024-08-22 21:40

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BattlefieldCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('winner', models.CharField(choices=[('Caldari', 'Caldari'), ('Gallente', 'Gallente'), ('Minmatar', 'Minmatar'), ('Amarr', 'Amarr')], max_length=10)),
                ('defender', models.CharField(choices=[('Caldari', 'Caldari'), ('Gallente', 'Gallente'), ('Minmatar', 'Minmatar'), ('Amarr', 'Amarr')], max_length=10)),
                ('system', models.CharField(max_length=100)),
                ('converted_to_scheduled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LiveBattlefield',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spawn_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('defender', models.CharField(choices=[('Caldari', 'Caldari'), ('Gallente', 'Gallente'), ('Minmatar', 'Minmatar'), ('Amarr', 'Amarr')], max_length=10)),
                ('fc', models.CharField(default='No planned FC', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ScanResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('result_string', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledBattlefield',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_time', models.DateTimeField(default=datetime.datetime(2024, 8, 23, 1, 40, 40, 885936, tzinfo=datetime.timezone.utc))),
                ('defender', models.CharField(choices=[('Caldari', 'Caldari'), ('Gallente', 'Gallente'), ('Minmatar', 'Minmatar'), ('Amarr', 'Amarr')], max_length=10)),
                ('fc', models.CharField(default='No planned FC', max_length=10)),
                ('is_between_noon_and_four_hours_after', models.BooleanField(default=False, editable=False)),
            ],
        ),
    ]
