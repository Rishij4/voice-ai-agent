import redis

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

def save_session(session_id, data):
    redis_client.set(session_id, str(data), ex=1800)

def get_session(session_id):
    return redis_client.get(session_id)