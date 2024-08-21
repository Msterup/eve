from .models import BattlefieldCompletion
from datetime import timedelta


def get_battlefield_timers():
    all_battlefields = BattlefieldCompletion.objects.all().order_by("-time")[:4]
    human_readable_battlefields = []
    for battlefield_data in all_battlefields:
        battlefield = {}
        battlefield["report_time"] = battlefield_data.time.strftime('%Y-%m-%d %H:%M:%S')
        battlefield["owner"] = battlefield_data.owner
        battlefield["spawn_time"] = (battlefield_data.time + timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')
        human_readable_battlefields.append(battlefield)


    return {"battlefields": human_readable_battlefields}