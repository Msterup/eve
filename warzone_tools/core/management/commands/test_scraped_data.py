

from battlefield_tracker.util.scraper.parser import consume_web_data
from datetime import datetime



from django.core.management.base import BaseCommand
from battlefield_tracker.models import BattlefieldCompletion

class Command(BaseCommand):
    help = "Add a test battlefield completion"

    def handle(self, *args, **options):
        system_data = {'status': 'Frontline', 'system': 'Nennamaila', 'defender': 'caldari', 'contested': '65.04', 'base_advantage': '6', 'update_advantage': True, 'gallente_objectives_advantage': 95, 'attacker': 'gallente', 'gallente_systems_advantage': 10, 'caldari_objectives_advantage': 49, 'caldari_systems_advantage': 40}
        data = {'Nennamaila': system_data,
                'faction': 'caldari',
                'timestamp': datetime.now().isoformat()}
        result = consume_web_data(data)
        print(result)