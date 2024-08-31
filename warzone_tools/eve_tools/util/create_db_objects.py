from eve_tools.models import BattlefieldCompletion, ScheduledBattlefield, SolarSystem
from django.utils import timezone
from datetime import time

def create_battlefield_completion(solar_system, winner_faction_id, defender_faction_id, fc_name=None):
    """
    Creates a BattlefieldCompletion record.
    
    Args:
    - solar_system: The SolarSystem instance where the battlefield took place.
    - winner_faction_id: The ID of the winning faction.
    - defender_faction_id: The ID of the defending faction.
    - fc_name: The name of the fleet commander (optional).
    """
    BattlefieldCompletion.objects.create(
        solar_system=solar_system,
        winner=winner_faction_id,
        defender=defender_faction_id,
        fc=fc_name,
        completion_time=timezone.now(),
    )

def create_scheduled_battlefield(defender_faction_id, battlefield_type='Normal', fc_name=None, expected_time=None, is_between_downtime_and_four_hours_after=None):
    """
    Creates a ScheduledBattlefield record.
    
    Args:
    - defender_faction_id: The ID of the defending faction.
    - battlefield_type: Type of the battlefield (Default is 'Normal').
    - fc_name: The name of the fleet commander (optional).
    - expected_time: The expected datetime for the battlefield (optional).
    """
    # Define the time range: 11:00 AM to 3:00 PM (4 hours after 11:00 AM)
    start_time = time(11, 0)  # 11:00 AM
    end_time = time(15, 0)    # 3:00 PM

    if expected_time is None:
        expected_time = timezone.now() + timezone.timedelta(hours=4)  # Example logic for expected time

    # Extract the time component of expected_time
    expected_time_time = expected_time.time()

    # Set is_between_downtime_and_four_hours_after to True if within the range
    if is_between_downtime_and_four_hours_after is None:
        is_between_downtime_and_four_hours_after = start_time <= expected_time_time <= end_time

    ScheduledBattlefield.objects.create(
        defender=defender_faction_id,
        fc=fc_name,
        spawn_time=timezone.now(),
        expected_time=expected_time,
        battlefield_type=battlefield_type,
        is_between_downtime_and_four_hours_after=is_between_downtime_and_four_hours_after
    )