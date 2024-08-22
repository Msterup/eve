import redis
from scraper.extractor import get_web_data
from battlefield_tracker.models import BattlefieldCompletion, ScanResult


def consume_web_data(data):
    redis_client = redis.StrictRedis(host='redis', port=6379, db=1)
    completed_battlefields = []    
    advantage_swing_sum = 0

    for row in data:
        key = row[1] # System name
        value = int(row[5].strip('%')) # Current advantage

        old_value = redis_client.get(key)
        if old_value is None:
            old_value = value # Handle no entries in database
        old_value = int(old_value)

        advantage_swing = old_value - value

        if abs(advantage_swing) > 13:
            # A battlefield has completed in this system!
            owner = row[0]
            winner = get_winner(old_value, value, owner)
            completion = BattlefieldCompletion.objects.create(owner=owner, winner=winner, system=row[1])
            completed_battlefields.append(completion)

        redis_client.set(key, value) # Updata database entry
        advantage_swing_sum += advantage_swing

    if completed_battlefields:
        result =  str(completed_battlefields)
    else:
        result = f"No completed battlefields detected, sum of swing is {advantage_swing_sum}"

    ScanResult.objects.create(result_string=result)
    return result # Propergate results up to caller (for logging to admin dashboard)


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

if __name__ == "__main__":
    data = get_web_data()
    consume_web_data(data)
