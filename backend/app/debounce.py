from app.database import redis_client


def is_duplicate(component_id):

    key = f"debounce:{component_id}"

    exists = redis_client.get(key)

    if exists:
        return True

    redis_client.setex(key, 10, "active")

    return False
