# === FILE: utils/query_cache.py ===
import redis.asyncio as redis
import hashlib
import json

cache = redis.Redis(host="localhost", port=6379, decode_responses=True)

def hash_query(query):
    return hashlib.sha256(query.encode()).hexdigest()

async def get_cached_response(query):
    return await cache.get(hash_query(query))

async def set_cached_response(query, response):
    await cache.set(hash_query(query), response, ex=3600)

