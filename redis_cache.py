import redis
import json
import logging


redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def get_cached_response(query: str):
    try: 
        cached = redis_client.get(query)
        if cached:
            logging.info(f"[Cache Hit] Query: {query}")
            return json.loads(cached)
        logging.info(f"[Cache Miss] Query: {query}")
        return None
    except Exception as e:
        logging.error(f"[Redis Error] Failed to get cache for query '{query}': {e}")
        return None


def set_cached_response(query: str, response: dict, expire_seconds=3600):
    try:
        redis_client.set(query, json.dumps(response), ex=expire_seconds)
        logging.info(f"[Cache Set] Cached response for query: {query}")
    except Exception as e:
        logging.error(f"[Redis Error] Failed to set cache for query '{query}': {e}")


