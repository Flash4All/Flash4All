import redis
import os
import time

host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
db = os.getenv("REDIS_DB")
password = None
if os.getenv("REDIS_PASSWORD") is not None:
    password = os.getenv("REDIS_PASSWORD")

redis_client = redis.StrictRedis(host=host, port=port, db=db, password=password)

def exists(key):
    return redis_client.exists(key)

def set(time):
    return lambda key, value : redis_client.set(key, value, time)

def hset(time):
    return lambda key, value : redis_client.hset(key, value, time)

def rpush(key, value):
    return redis_client.rpush(key, value)

def lpush(key, value):
    return redis_client.lpush(key, value)

" duplicate of rpush "
def push(key, value):
    return rpush(key, value)

def hgetall(key):
    return redis_client.hgetall(key)

def delete(key):
    return redis_client.delete(key)

def lpop(key):
    return redis_client.lpop(key)

def rpop(key):
    return redis_client.rpop(key)

def pop(key):
    return redis_client.lpop(key)

def get(key):
    return redis_client.get(key)

def getall(key):
    return redis_client.lrange(key, 0, -1)

def flush_db():
    if os.getenv("ENV") == "test":
        redis_client.flushdb()
    else:
        raise

set_one_minute = set(60)
set_five_minutes = set(60 * 5)
set_hour = set(60*60)
set_day = set(60*60*24)
set_week = set(60*60*24*7)
set_forever = set(None)
