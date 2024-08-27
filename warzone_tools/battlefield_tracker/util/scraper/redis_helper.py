def update_advantage_in_redis(redis_client, system, key, values):
    advantage = int(values[key])
    redis_key = f"{system}_{key}"

    old_advantage = redis_client.get(redis_key)
    if old_advantage is None:
        old_advantage = 100 # Handle no entries in database, ask for full system scan
    old_advantage = int(old_advantage)

    advantage_swing = abs(old_advantage - advantage)
    redis_client.set(redis_key, advantage) # Updata database entry

    return advantage_swing