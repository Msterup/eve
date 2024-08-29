if __name__ == "__main__": # for local debug
    import sys, os, django
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

from django.utils import timezone
from eve_tools.util.create_db_objects import create_battlefield_completion, create_scheduled_battlefield
import requests
from eve_tools.models import SolarSystem, FactionAdvantage, ScheduledBattlefield

def get_web_data():
    url = "https://www.eveonline.com/api/warzone/status"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        warzone_data = response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        warzone_data = None
    update_all_systems(warzone_data)


def update_all_systems(warzone_data):
    for system_data in warzone_data:
        # Fetch or create the solar system
        solarsystem_id = system_data['solarsystemID']
        system, created = SolarSystem.objects.get_or_create(solarsystem_id=solarsystem_id)
        old_occupier = system.occupier_faction

        # Update system attributes if they have changed
        system.owner_faction = system_data['ownerFaction']
        system.occupier_faction = system_data['occupierFaction']
        system.contested_status = system_data['contestedStatus']
        system.contested_amount = system_data['contestedAmount']
        system_delta = system.save()  # This triggers the pre-save hook to track changes
        if system_delta and system_delta.occupier_faction and not created:
            create_scheduled_battlefield(
                defender_faction_id=old_occupier,
                battlefield_type='System Flipped',  # Since the system's occupier changed
                expected_time=timezone.now(), # Spawn imediately
                fc_name=None  # Or use actual FC name if available
            )
        
        # Update faction advantages
        for advantage_data in system_data['advantage']:
            faction_id = advantage_data['factionID']
            
            # Fetch or create the faction advantage
            advantage, adv_created = FactionAdvantage.objects.get_or_create(
                solar_system=system, faction_id=faction_id
            )

            # Update advantage attributes if they have changed
            advantage.terrain_amount = advantage_data['terrainAmount']
            advantage.dynamic_amount = advantage_data['dynamicAmount']
            advantage.total_amount = advantage_data['totalAmount']
            adv_delta = advantage.save()  # This triggers the pre-save hook to track changes

            if adv_delta and not adv_created:
                if adv_delta.dynamic_amount is not None:
                    if adv_delta.dynamic_amount > 5:
                        # Create battlefield completion (example)
                        create_battlefield_completion(
                            solar_system=system,
                            winner_faction_id=advantage.faction_id,
                            defender_faction_id=system.occupier_faction,
                            fc_name=None  # Or use actual FC name if available
                        )
                        create_scheduled_battlefield(
                            defender_faction_id=faction_id,
                            battlefield_type='Normal',
                            fc_name=None  # Or use actual FC name if available
                            )
                        # Find the oldest scheduled battlefield that meets the conditions
                        oldest_battlefield = ScheduledBattlefield.objects.filter(
                            expected_time__lt=timezone.now(),  # Only consider battlefields where the expected time has passed
                            defender=old_occupier, # Match the occupier_faction with the defender
                        ).order_by('spawn_time').first()

                        # If an appropriate battlefield is found, delete it
                        if oldest_battlefield:
                            oldest_battlefield.delete()

if __name__ == "__main__":

    FactionAdvantage.objects.filter(faction_id=500002, solar_system__solarsystem_id=30002056).update(dynamic_amount=-13)
    get_web_data()