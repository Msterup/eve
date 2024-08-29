
from django.core.management.base import BaseCommand
from eve_tools.models import BattlefieldCompletion

class Command(BaseCommand):
    help = "Add a test battlefield completion"

    def handle(self, *args, **options):
        completion = BattlefieldCompletion.objects.create(defender="caldari", winner='caldari', system="Jita")