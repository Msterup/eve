from django.db import models
from django.utils import timezone
# Create your models here.


class BattlefieldCompletion(models.Model):
    WINNER_CHOICES = [
        ('Caldari', 'Caldari'),
        ('Gallente', 'Gallente'),
        ('Minmatar', 'Minmatar'),
        ('Amarr', 'Amarr'),
    ]
    
    time = models.DateTimeField(default=timezone.now)
    winner = models.CharField(max_length=10, choices=WINNER_CHOICES)
    owner = models.CharField(max_length=10, choices=WINNER_CHOICES)
    system = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.system} - {self.winner} at {self.time}'
    

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