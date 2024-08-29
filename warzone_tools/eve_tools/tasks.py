import datetime
from django.utils import timezone
from django.db import models

from eve_tools.models import ScheduledBattlefield
from eve_tools.util.parser import get_web_data
from eve_tools.util.create_db_objects import create_scheduled_battlefield

def report_completed_battlefields():
    get_web_data()

def create_downtime_scheduled_battlefields():
    to_create = [500001, 500002, 500003, 500004]
    
    for defender in to_create:
        create_scheduled_battlefield(
            defender_faction_id=defender,
            battlefield_type='Downtime',  # Since the system's occupier changed
            fc_name=None  # Or use actual FC name if available
        )

def delete_non_downtime_battlefields():
    """
    Deletes all ScheduledBattlefield records that are not of type 'Downtime'.
    """
    ScheduledBattlefield.objects.filter(~models.Q(battlefield_type='Downtime')).delete()

    