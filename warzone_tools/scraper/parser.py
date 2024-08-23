import redis
from scraper.extractor import get_web_data
from battlefield_tracker.models import BattlefieldCompletion, ScanResult, LiveBattlefield


def consume_web_data(data):
    redis_client = redis.StrictRedis(host='redis', port=6379, db=1)
    completed_battlefields = []    
    advantage_swing_sum = 0
    results = []

    # Look for battlefields
    for row in data:
        key = row[1] # System name
        value = int(row[5].strip('%')) # Current advantage

        old_value = redis_client.get(key)
        if old_value is None:
            old_value = value # Handle no entries in database
        old_value = int(old_value)

        advantage_swing = old_value - value

        if abs(advantage_swing) > 12:
            # A battlefield has completed in this system!
            owner = row[0]
            winner = get_winner(old_value, value, owner)
            completion = BattlefieldCompletion.objects.create(defender=owner, winner=winner, system=row[1])
            completed_battlefields.append(completion)

            results.append(remove_live_battlefields(defender=owner))

        redis_client.set(key, value) # Updata database entry
        advantage_swing_sum += advantage_swing

    if completed_battlefields:
        results.append(str(completed_battlefields))
    else:
        results.append(f"No completed battlefields detected, sum of swing is {advantage_swing_sum}")
    ScanResult.objects.create(result_string=results)

    redis_client = redis.StrictRedis(host='redis', port=6379, db=2) # New database so I can use the same keynames
    # Look for system captures
    for row in data:
        key = row[1] # System name
        new_owner = row[0]

        old_owner = redis_client.get(key)
        if old_owner is None:
            old_owner = value # Handle no entries in database

        if old_owner != new_owner:
            # A system has flipped
            LiveBattlefield.objects.create(defender=old_owner)
            results.append("Created live battledfield")


    return results # Propergate results up to caller (for logging to admin dashboard)


def get_winner(old_value, value, owner):
    if old_value < value:
        return owner
    else:
        if owner == "Caldari":
            return "Gallente"
        if owner == "Gallente":
            return "Caldari"
        if owner == "Minmatar":
            return "Amarr"
        if owner == "Amarr":
            return "Minmatar"

def remove_live_battlefields(defender):
    oldest_battlefield = LiveBattlefield.objects.filter(defender=defender).order_by('spawn_time').first()
    if oldest_battlefield:
        result = f"Deleting a live battlefield with spawn time {oldest_battlefield.spawn_time}" 
        oldest_battlefield.delete()
    else:
        result = "No live battlefields found to delete!"
    return result

if __name__ == "__main__":
    data = get_web_data()
    consume_web_data(data)
