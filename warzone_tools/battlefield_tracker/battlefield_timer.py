from .models import BattlefieldCompletion, ScheduledBattlefield, LiveBattlefield
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone

# todo: add timed cache here 
def get_battlefield_timers(faction):

    faction = faction.capitalize()
    if faction in ['caldari', 'gallente']:
        faction_query = Q(defender='caldari') | Q(defender='gallente')
    elif faction in ['minmatar', 'amarr']:
        faction_query = Q(defender='minmatar') | Q(defender='amarr')
    else:
        faction_query = Q()

    result = {}

    # Historic battlefields
    all_battlefields = BattlefieldCompletion.objects.all().filter(faction_query).order_by("-completion_time")
    historic_readable_battlefields = []
    for battlefield_data in all_battlefields:
        battlefield = {}
        battlefield["report_time"] = battlefield_data.completion_time.strftime('%Y-%m-%d %H:%M:%S')
        battlefield["defender"] = battlefield_data.defender
        battlefield["winner"] = battlefield_data.winner
        battlefield["system"] = battlefield_data.system
        battlefield["spawn_time"] = (battlefield_data.completion_time + timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')
        historic_readable_battlefields.append(battlefield)

    result["historic_battlefields"] = historic_readable_battlefields

    # Scheduled battlefields
    cutoff_time = timezone.now() - timedelta(hours=4)

    all_battlefields = ScheduledBattlefield.objects.all().filter(
        faction_query,
        expected_time__gte=cutoff_time,
        is_between_downtime_and_four_hours_after=True,
        ).order_by("-expected_time")
    
    scheduled_readable_battlefields = []
    for battlefield_data in all_battlefields:
        battlefield = {}
        battlefield["expected_time"] = battlefield_data.expected_time.strftime('%Y-%m-%d %H:%M:%S')
        battlefield["defender"] = battlefield_data.defender
        battlefield["fc"] = battlefield_data.fc
        battlefield["battlefield_type"] = battlefield_data.battlefield_type
        scheduled_readable_battlefields.append(battlefield)

    result["scheduled_battlefields"] = scheduled_readable_battlefields
    
    # Live battlefields
    all_battlefields = LiveBattlefield.objects.all().filter(faction_query).order_by("-spawn_time")[:4]
    live_readable_battlefields = []
    for battlefield_data in all_battlefields:
        battlefield = {}
        battlefield["spawn_time"] = battlefield_data.spawn_time.strftime('%Y-%m-%d %H:%M:%S')
        battlefield["defender"] = battlefield_data.defender
        battlefield["fc"] = battlefield_data.fc
        live_readable_battlefields.append(battlefield)

    result["live_battlefields"] = live_readable_battlefields

    # TODO: Find and report systems with advantage making them undetectable

    return result