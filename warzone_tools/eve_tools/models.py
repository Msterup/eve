from django.db import models
from django.utils import timezone
from datetime import time
# Create your models here.

from django.db import models

class SolarSystem(models.Model):
    solarsystem_id = models.PositiveIntegerField(unique=True)
    owner_faction = models.PositiveIntegerField(null=True)
    occupier_faction = models.PositiveIntegerField(null=True)
    contested_status = models.CharField(max_length=50, null=True)
    contested_amount = models.FloatField(null=True)

    def __str__(self):
        return f"Solar System {self.solarsystem_id}"
    
    def save(self, *args, **kwargs):
        delta = None
        if self.pk:  # Check if this is an update (existing record)
            previous = SolarSystem.objects.get(pk=self.pk)
            delta_fields = {}
            if previous.owner_faction != self.owner_faction:
                delta_fields['owner_faction'] = self.owner_faction
            if previous.occupier_faction != self.occupier_faction:
                delta_fields['occupier_faction'] = self.occupier_faction
            if previous.contested_status != self.contested_status:
                delta_fields['contested_status'] = self.contested_status
            if previous.contested_amount != self.contested_amount:
                delta_fields['contested_amount'] = self.contested_amount
            
            if delta_fields:
                delta = SolarSystemDelta.objects.create(
                    solar_system=self, 
                    timestamp=timezone.now(), 
                    **delta_fields
                )

        super().save(*args, **kwargs)
        return delta

class FactionAdvantage(models.Model):
    solar_system = models.ForeignKey(SolarSystem, related_name='advantages', on_delete=models.CASCADE)
    faction_id = models.PositiveIntegerField(null=True)
    terrain_amount = models.FloatField(null=True)
    dynamic_amount = models.FloatField(null=True)
    total_amount = models.FloatField(null=True)

    def __str__(self):
        return f"Advantage for Faction {self.faction_id} in System {self.solar_system.solarsystem_id}"
    
    def save(self, *args, **kwargs):
        delta = None
        if self.pk:  # Check if this is an update (existing record)
            previous = FactionAdvantage.objects.get(pk=self.pk)
            delta_fields = {}
            
            def calculate_delta(field_name):
                previous_value = getattr(previous, field_name)
                current_value = getattr(self, field_name)
                if previous_value != current_value:
                    delta_fields[field_name] = (current_value or 0) - (previous_value or 0)

            # Apply the delta calculation to each field
            calculate_delta('terrain_amount')
            calculate_delta('dynamic_amount')
            calculate_delta('total_amount')
            
            if delta_fields:
                delta = FactionAdvantageDelta.objects.create(
                    faction_advantage=self, 
                    timestamp=timezone.now(), 
                    **delta_fields
                )

        super().save(*args, **kwargs)
        return delta

class SolarSystemDelta(models.Model):
    solar_system = models.ForeignKey(SolarSystem, related_name='deltas', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    owner_faction = models.PositiveIntegerField(null=True, blank=True)
    occupier_faction = models.PositiveIntegerField(null=True, blank=True)
    contested_status = models.CharField(max_length=50, null=True, blank=True)
    contested_amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Delta for System {self.solar_system.solarsystem_id} at {self.timestamp}"


class FactionAdvantageDelta(models.Model):
    faction_advantage = models.ForeignKey(FactionAdvantage, related_name='deltas', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    terrain_amount = models.FloatField(null=True, blank=True)
    dynamic_amount = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Delta for Faction {self.faction_advantage.faction_id} in System {self.faction_advantage.solar_system.solarsystem_id} at {self.timestamp}"

TYPE_CHOICES = [
    ('Downtime', 'Downtime'),
    ('Normal', 'Normal'),
    ('System Flipped', 'System Flipped'),
]

class BattlefieldCompletion(models.Model):
    completion_time = models.DateTimeField(default=timezone.now)
    winner = models.PositiveIntegerField()
    defender = models.PositiveIntegerField()
    solar_system = models.ForeignKey(SolarSystem, related_name='BattlefieldCompletion', on_delete=models.CASCADE)
    fc = models.CharField(max_length=100, default=None, blank=True, null=True)

    def delete_old_records(cls, days=3):
        """Delete records older than the specified number of days."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        cls.objects.filter(completion_time__lt=cutoff_date).delete()

    def __str__(self):
        return f"BattlefieldCompletion in {self.solar_system} at {self.completion_time}"


class ScheduledBattlefield(models.Model):
    TYPE_CHOICES = [
        ('Downtime', 'Downtime'),
        ('Normal', 'Normal'),
        ('System Flipped', 'System Flipped'),
    ]
    battlefield_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='Normal')
    defender = models.PositiveIntegerField()
    fc = models.CharField(max_length=100, default=None, blank=True, null=True)
    spawn_time = models.DateTimeField(default=timezone.now) # Aka report time
    expected_time = models.DateTimeField(default=timezone.now)
    is_between_downtime_and_four_hours_after = models.BooleanField(editable=True, default=False)

    def delete_old_records(cls, days=3):
        """Delete records older than the specified number of days."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        cls.objects.filter(expected_time__lt=cutoff_date).delete()

    def __str__(self):
        return f"ScheduledBattlefield ({self.battlefield_type}) for {self.defender} at {self.expected_time}"