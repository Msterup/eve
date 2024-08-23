
from django.core.management.base import BaseCommand
from battlefield_tracker.models import BattlefieldCompletion

class Command(BaseCommand):
    help = "Add a test battlefield completion"

    def handle(self, *args, **options):
        completion = BattlefieldCompletion.objects.create(defender="Caldari", winner='Caldari', system="Jita")