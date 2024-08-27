
from datetime import datetime
from django.utils import timezone
import redis
if __name__ == "__main__": # for local debug
    import sys, os, django
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
from battlefield_tracker.util.scraper.extractor import get_adv_data
from battlefield_tracker.util.scraper.redis_helper import update_advantage_in_redis
from battlefield_tracker.models import AM_System, CG_System, BattlefieldCompletion, LiveBattlefield

    
def remove_oldest_live_battlefield(defender):
    oldest_battlefield = LiveBattlefield.objects.filter(defender=defender).order_by('spawn_time').first()
    if oldest_battlefield:
        result = f"Deleting a live battlefield with spawn time {oldest_battlefield.spawn_time}"
        oldest_battlefield.delete()
    else:
        result = "No live battlefields found to delete!"
    return result

def consume_web_data(data):
    # TODO: Refactor and make several steps
    redis_client = redis.StrictRedis(host='redis', port=6379, db=1)
    results = []
    timestamp = data.get("timestamp")
    if timestamp:
        # Parse the timestamp string to a datetime object
        completion_time = datetime.fromisoformat(timestamp)
        completion_time = timezone.make_aware(completion_time, timezone.get_current_timezone())
    else:
        completion_time = timezone.now()

    # Look for battlefields

    for system_name, system_data in data.items():
        if system_name in ['timestamp', 'faction']:
            continue
        if system_data['defender'] in ['caldari', 'gallente']:
            ModelClass = CG_System
            field_map = {
                'caldari_objectives_advantage': 'caldari_objectives_advantage',
                'gallente_objectives_advantage': 'gallente_objectives_advantage',
                'caldari_systems_advantage': 'caldari_systems_advantage',
                'gallente_systems_advantage': 'gallente_systems_advantage'
            }
        else:
            ModelClass = AM_System
            field_map = {
                'amarr_objectives_advantage': 'amarr_objectives_advantage',
                'minmatar_objectives_advantage': 'minmatar_objectives_advantage',
                'amarr_systems_advantage': 'amarr_systems_advantage',
                'minmatar_systems_advantage': 'minmatar_systems_advantage'
            }

        # Prepare the defaults dynamically based on the field_map ??? what
        defaults = {
            'status': system_data['status'],
            'contested': system_data['contested'],
            'base_advantage': system_data['base_advantage'],
        }
        # advanced_advantage = {
        #     field_map['caldari_objectives_advantage']: system_data.get('caldari_objectives_advantage', 0),
        #     field_map['gallente_objectives_advantage']: system_data.get('gallente_objectives_advantage', 0),
        #     field_map['caldari_systems_advantage']: system_data.get('caldari_systems_advantage', 0),
        #     field_map['gallente_systems_advantage']: system_data.get('gallente_systems_advantage', 0),
        # }

        # Using get_or_create to either get an existing record or create a new one
        obj, created = ModelClass.objects.get_or_create(
            name=system_data['system'],
            defaults=defaults
        )
        if system_data["update_advantage"]:
            # Advantage data is to be 

            for original_field, mapped_field in field_map.items():
                if "objective" in original_field:
                    swing = update_advantage_in_redis(redis_client, system_data['system'], mapped_field, system_data)
                    if swing > 3:
                        if "caldari" in original_field:
                            winner = 'caldari'
                        elif "gallente" in original_field:
                            winner = 'gallente'
                        elif "amarr" in original_field:
                            winner = 'amarr'
                        else:
                            winner = 'minmatar'
                        
                        BattlefieldCompletion.objects.create(
                            completion_time=completion_time,
                            winner=winner,
                            defender=system_data['defender'],
                            system=system_data['system']
                        )

                        # Call the remove_oldest_live_battlefield function
                        remove_result = remove_oldest_live_battlefield(defender=system_data["defender"])
                        results.append(remove_result)

                        results.append(f"BattlefieldCompletion created for system {system_data['system']} with winner {winner}")
                        results.append(f"Significant swing detected for {mapped_field}: {swing}")
        
        if not created:
            update_data = {}

            # Check and update each mapped field
            for original_field, mapped_field in field_map.items():
                current_value = getattr(obj, mapped_field)
                new_value = system_data.get(original_field, current_value)
                if current_value != new_value:
                    update_data[mapped_field] = new_value

            # Check and update additional fields
            if obj.status != system_data['status']:
                update_data['status'] = system_data['status']

            if obj.contested != system_data['contested']:
                update_data['contested'] = system_data['contested']
            
            if obj.contested != system_data['base_advantage']:
                update_data['base_advantage'] = system_data['base_advantage']

            update_data['last_updated'] = completion_time  # Always update the last_updated field

            ModelClass.objects.filter(pk=obj.pk).update(**update_data)

        results.append(f"System {'created' if created else 'updated'}: {obj.name}.")

    return results # Propergate results up to caller (for logging to admin dashboard)

if __name__ == "__main__":
    data = get_adv_data("caldari")
    consume_web_data(data)
