from django.db import models
from django.utils import timezone
from datetime import timedelta, time
# Create your models here.


FACTION_CHOICES = [
        ('Caldari', 'Caldari'),
        ('Gallente', 'Gallente'),
        ('Minmatar', 'Minmatar'),
        ('Amarr', 'Amarr'),
    ]

class BattlefieldCompletion(models.Model):
    completion_time = models.DateTimeField(default=timezone.now)
    winner = models.CharField(max_length=10, choices=FACTION_CHOICES)
    defender = models.CharField(max_length=10, choices=FACTION_CHOICES)
    system = models.CharField(max_length=100)
    converted_to_scheduled = models.BooleanField(default=False)

    @classmethod
    def delete_old_records(cls, days=3):
        """Delete records older than the specified number of days."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        cls.objects.filter(time__lt=cutoff_date).delete()

class ScheduledBattlefield(models.Model):
    default_time = timezone.now() + timedelta(hours=4)
    expected_time = models.DateTimeField(default=default_time)
    defender = models.CharField(max_length=10, choices=FACTION_CHOICES)
    fc = models.CharField(max_length=10, default="No planned FC")

    is_between_noon_and_four_hours_after = models.BooleanField(editable=False, default=False)
    
    def save(self, *args, **kwargs):
        # Define the time range: Noon to 4 hours after noon
        start_time = time(12, 0)  # 12:00 PM (Noon)
        end_time = (timezone.now() + timedelta(hours=4)).time()
        
        # Calculate if expected_time is between start_time and end_time
        expected_time_in_time = self.expected_time.time()
        self.is_between_noon_and_four_hours_after = start_time <= expected_time_in_time <= end_time
        
        # Call the original save method
        super().save(*args, **kwargs)
    
    @classmethod
    def delete_old_records(cls, days=3):
        """Delete records older than the specified number of days."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        cls.objects.filter(time__lt=cutoff_date).delete()

class LiveBattlefield(models.Model):
    spawn_time = models.DateTimeField(default=timezone.now)
    defender = models.CharField(max_length=10, choices=FACTION_CHOICES)
    fc = models.CharField(max_length=10, default="No planned FC")
    
    @classmethod
    def delete_old_records(cls, days=3):
        """Delete records older than the specified number of days."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        cls.objects.filter(time__lt=cutoff_date).delete()

class ScanResult(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    result_string = models.CharField(max_length=255)

    def __str__(self):
        return f"Scan at {self.time} - Result: {self.result_string}"
        
    @classmethod
    def delete_old_records(cls, days=3):
        """Delete records older than the specified number of days."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        cls.objects.filter(time__lt=cutoff_date).delete()