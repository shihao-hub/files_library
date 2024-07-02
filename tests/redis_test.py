import redis
from redis import StrictRedis as Redis

client = Redis("127.0.0.1", 6379, 0)
print(client)
print(client.get("name"))
print(client.get("drafts"))
client.set("drafts", )
print(client.get("drafts"))
