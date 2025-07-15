import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def append_to_history(user_id, query, sql_query, inference, response_df):
    session_key = f"session:{user_id}:history"

    entry = {
        "query": query,
        "sql_query": sql_query,
        "inference": inference,
        "response": response_df.to_dict(orient="records")
    }

    r.rpush(session_key, json.dumps(entry))

def get_history(user_id):
    session_key = f"session:{user_id}:history"
    entries = r.lrange(session_key, 0, -1)
    return [json.loads(e) for e in entries]

def clear_history(user_id):
    session_key = f"session:{user_id}:history"
    r.delete(session_key)
