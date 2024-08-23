from scraper.extractor import get_web_data
from scraper.parser import consume_web_data
from datetime import timedelta
from django.utils import timezone

from .models import BattlefieldCompletion, ScheduledBattlefield, LiveBattlefield

def report_completed_battlefields():
    data = get_web_data()
    result = consume_web_data(data)
    return result # For reporting in admin dashboard

def convert_historic_to_scheduled_battlefield():
    # Retrieve the last five BattlefieldCompletion records
    last_five_completions = BattlefieldCompletion.objects.filter(
        converted_to_scheduled=False
    ).order_by('-completion_time')[:5]

    results = []

    for completion in last_five_completions:
        # Calculate the expected_time as 4 hours after the completion time
        expected_time = completion.completion_time + timedelta(hours=4)

        # Use get_or_create to ensure that we don't create duplicates
        scheduled_battlefield, created = ScheduledBattlefield.objects.get_or_create(
            expected_time=expected_time,
            defender=completion.defender,
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
    scheduled_battlefields = ScheduledBattlefield.objects.filter(expected_time__gte=current_time)
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
        result = f"LiveBattlefield {'created' if created else 'already exists'} for {scheduled.defender} at {scheduled.expected_time}"
        print(result)
        results.append(result)

        # Collect the ScheduledBattlefield to delete
        to_delete.append(scheduled)

    # Delete the scheduled battlefields after processing
    for scheduled in to_delete:
        scheduled.delete()

    return results

if __name__ == "__main__":
    report_completed_battlefields()

