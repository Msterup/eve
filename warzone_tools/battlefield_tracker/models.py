from django.db import models
from django.utils import timezone
from datetime import time
# Create your models here.


FACTION_CHOICES = [
        ('caldari', 'caldari'),
        ('gallente', 'gallente'),
        ('minmatar', 'minmatar'),
        ('amarr', 'amarr'),
    ]

SYSTEM_STATUS = [
    ("Frontline", "Frontline"),
    ("Command Operations", "Command Operations"),
    ("Rearguard", "Rearguard"),
]

class System(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    status = models.CharField(max_length=255, choices=SYSTEM_STATUS)
    contested = models.DecimalField(max_digits=5, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True) 
    base_advantage = models.PositiveSmallIntegerField(blank=False)

    class Meta:
        abstract = True

class CG_System(System):
    caldari_objectives_advantage = models.PositiveSmallIntegerField(blank=True)
    gallente_objectives_advantage = models.PositiveSmallIntegerField(blank=True)
    caldari_systems_advantage = models.PositiveSmallIntegerField(blank=True)
    gallente_systems_advantage = models.PositiveSmallIntegerField(blank=True)

class AM_System(System):
    amarr_objectives_advantage = models.PositiveSmallIntegerField(blank=True)
    minmatar_objectives_advantage = models.PositiveSmallIntegerField(blank=True)
    amarr_systems_advantage = models.PositiveSmallIntegerField(blank=True)
    minmatar_systems_advantage = models.PositiveSmallIntegerField(blank=True)

# Base class for all models that require the delete_old_records method
class Record(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def delete_old_records(cls, days=3):
        """Delete records older than the specified number of days."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        cls.objects.filter(time__lt=cutoff_date).delete()

# Base class for all battlefield-related models
class Battlefield(Record):
    completion_time = models.DateTimeField(default=timezone.now)
    winner = models.CharField(max_length=10, choices=FACTION_CHOICES, blank=True)
    defender = models.CharField(max_length=10, choices=FACTION_CHOICES)
    system = models.CharField(max_length=100, blank=True)
    fc = models.CharField(max_length=100, default=None, blank=True)

    class Meta:
        abstract = True

# Derived class for completed battlefields
class BattlefieldCompletion(Battlefield):
    # Also known as historic battlefields
    converted_to_scheduled = models.BooleanField(default=False)

# Derived class for scheduled battlefields
class ScheduledBattlefield(Battlefield):
    TYPE_CHOICES = [
        ('Downtime', 'Downtime'),
        ('Normal', 'Normal'),
        ('System Flipped', 'System Flipped'),
    ]
    battlefield_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='Normal')
    default_time = models.DateField(default=timezone.now)
    expected_time = models.DateTimeField(default=timezone.now)
    is_between_downtime_and_four_hours_after = models.BooleanField(editable=False, default=False)
    def save(self, *args, **kwargs):
        # Define the time range: 11:00 AM to 3:00 PM (4 hours after 11:00 AM)
        start_time = time(11, 0)  # 11:00 AM
        end_time = time(15, 0)  # 3:00 PM
        
        # Extract the time component of expected_time
        expected_time_in_time = self.expected_time.time()

        # Set is_between_downtime_and_four_hours_after to True if within the range
        self.is_between_downtime_and_four_hours_after = start_time <= expected_time_in_time <= end_time
        
        # Call the original save method
        super().save(*args, **kwargs)

# Derived class for live battlefields
class LiveBattlefield(Battlefield):
    spawn_time = models.DateTimeField(default=timezone.now)

# Class for storing scan results
class ScanResult(Record):
    time = models.DateTimeField(auto_now_add=True)
    result_string = models.CharField(max_length=255)

    def __str__(self):
        return f"Scan at {self.time} - Result: {self.result_string}"

