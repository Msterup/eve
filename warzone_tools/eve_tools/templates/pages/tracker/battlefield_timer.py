if __name__ == "__main__": # for local debug
    import sys, os, django
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

from eve_tools.models import BattlefieldCompletion, ScheduledBattlefield, SolarSystem, FactionAdvantage
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from eve_tools.util.ids import EveIDTranslator


# todo: add timed cache here 
def get_battlefield_timers(faction):
    current_time = timezone.now()
    # Construct the faction query based on the input faction
    faction_query = Q()
    if faction in ['caldari', 'gallente']:
        faction_query = Q(defender__in=[500001, 500004])
    elif faction in ['minmatar', 'amarr']:
        faction_query = Q(defender__in=[500002, 500003])

    result = {}
    faction_id_query = Q()
    if faction in ['caldari', 'gallente']:
        faction_id_query = Q(faction_id__in=[500001, 500004])
    elif faction in ['minmatar', 'amarr']:
        faction_id_query = Q(faction_id__in=[500002, 500003])
    #TODO: make faction_id and faction the same thing

    # Query for frontline systems with a FactionAdvantage of 95 or above
    advantages = FactionAdvantage.objects.filter(
        total_amount__gte=95
    ).filter(faction_id_query)
    
    advantage_warnings = []
    for advantage in advantages:
        warning = {
            "faction": translate_faction_id(advantage.faction_id),
            "system": translate_system_id(advantage.solar_system.solarsystem_id),
        }
        advantage_warnings.append(warning)
    result["advantage_warnings"] = advantage_warnings

    # Historic battlefields
    all_battlefields = BattlefieldCompletion.objects.filter(faction_query).order_by("-completion_time")
    historic_readable_battlefields = []
    for battlefield_data in all_battlefields:
        battlefield = {
            "report_time": battlefield_data.completion_time.strftime('%Y-%m-%d %H:%M:%S'),
            "defender": translate_faction_id(battlefield_data.defender),
            "winner": translate_faction_id(battlefield_data.winner),
            "system": translate_system_id(battlefield_data.solar_system.solarsystem_id),
            "spawn_time": (battlefield_data.completion_time + timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'),
            "id": battlefield_data.solar_system.solarsystem_id,
        }
        historic_readable_battlefields.append(battlefield)

    result["historic_battlefields"] = historic_readable_battlefields

    # Scheduled battlefields
    all_battlefields = ScheduledBattlefield.objects.filter(
        faction_query,
        expected_time__gt=current_time,
        is_between_downtime_and_four_hours_after=False,
    ).order_by("expected_time")
    scheduled_readable_battlefields = []
    for battlefield_data in all_battlefields:
        battlefield = {
            "expected_time": battlefield_data.expected_time.strftime('%Y-%m-%d %H:%M:%S'),
            "defender": translate_faction_id(battlefield_data.defender),
            "fc": battlefield_data.fc,
            "battlefield_type": battlefield_data.battlefield_type,
            "id": battlefield_data.id,
        }
        scheduled_readable_battlefields.append(battlefield)

    result["scheduled_battlefields"] = scheduled_readable_battlefields
    
    # Live battlefields
    all_battlefields = ScheduledBattlefield.objects.filter(faction_query, expected_time__lt=current_time)
    live_readable_battlefields = []
    for battlefield_data in all_battlefields:
        battlefield = {
            "expected_time": battlefield_data.expected_time.strftime('%Y-%m-%d %H:%M:%S'),
            "battlefield_type": battlefield_data.battlefield_type,
            "defender": translate_faction_id(battlefield_data.defender),
            "fc": battlefield_data.fc,
            "id": battlefield_data.id,
        }
        live_readable_battlefields.append(battlefield)

    result["live_battlefields"] = live_readable_battlefields

    return result

def translate_faction_id(faction_id):
    """Translate faction ID to human-readable name."""
    return EveIDTranslator.translate_id(faction_id).capitalize()

def translate_system_id(system_id):
    """Translate system ID to human-readable name."""
    return EveIDTranslator.translate_id(system_id)

if __name__ == "__main__":
    result = get_battlefield_timers("caldari")
