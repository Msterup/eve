import datetime
from django.utils import timezone

from battlefield_tracker.util.scraper.extractor import get_adv_data
from battlefield_tracker.util.scraper.parser import consume_web_data
from .models import BattlefieldCompletion, ScheduledBattlefield, LiveBattlefield

def report_completed_battlefields(faction, status):
    data = get_adv_data(faction, status)
    result = consume_web_data(data)
    return data

def create_downtime_scheduled_battlefields():
    results = []
    to_create = ['caldari', 'gallente', "minmatar", "amarr"]
    
    for defender in to_create:
        scheduled_battlefield, created = ScheduledBattlefield.objects.get_or_create(
            expected_time=datetime.datetime.combine(timezone.now().date(), datetime.time(11, 0)),
            defender=defender,
            battlefield_type="Downtime",
            defaults={
                'fc': None,
            }
        )
        results.append(scheduled_battlefield)
    return results

def convert_historic_to_scheduled_battlefield():
    # Retrieve the last five BattlefieldCompletion records
    last_five_completions = BattlefieldCompletion.objects.filter(
        converted_to_scheduled=False
    ).order_by('-completion_time')[:5]

    results = []

    for completion in last_five_completions:
        # TODO: Check typs on this, it will not go in database 
        expected_time = completion.completion_time + datetime.timedelta(hours=4)

        # Use get_or_create to ensure that we don't create duplicates
        scheduled_battlefield, created = ScheduledBattlefield.objects.get_or_create(
            expected_time=expected_time,
            defender=completion.defender,
            system=completion.system,
            battlefield_type="Normal",
            defaults={
                'fc': None,
            }
        )

        # If the ScheduledBattlefield is newly created, mark the BattlefieldCompletion as converted
        if created:
            completion.converted_to_scheduled = True
            completion.save()

        # Log the result
        result = f"ScheduledBattlefield {'created' if created else 'already exists'} for {completion.defender} at {expected_time}"
        print(result)
        results.append(result)

    return results

def convert_scheduled_to_live_battlefield():
    results = []
    # Get the current time
    current_time = timezone.now()

    # Filter scheduled battlefields where the expected_time has passed
    scheduled_battlefields = ScheduledBattlefield.objects.filter(expected_time__lte=current_time)
    if not scheduled_battlefields:
        return "No scheduled battlefields to convert"


    to_delete = []


    for scheduled in scheduled_battlefields:
        # Create a corresponding LiveBattlefield
        live_battlefield, created = LiveBattlefield.objects.get_or_create(
            spawn_time=scheduled.expected_time,
            defender=scheduled.defender,
            defaults={
                'fc': scheduled.fc,  # Carry over the FC if any
            }
        )

        # Log the result
        results.append(f"LiveBattlefield {'created' if created else 'already exists'} for {scheduled.defender} at {scheduled.expected_time}")

        # Collect the ScheduledBattlefield to delete
        to_delete.append(scheduled)

    # Delete the scheduled battlefields after processing
    for scheduled in to_delete:
        scheduled.delete()
    # TODO: fix returns
    return results

if __name__ == "__main__":
    factions = ["caldari", "amarr"]
    for faction in factions:
        report_completed_battlefields(faction, "Frontline")

