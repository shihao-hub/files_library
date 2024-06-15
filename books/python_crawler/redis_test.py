from redis import StrictRedis as Redis

# , password="foobared"
#   redis.exceptions.ResponseError: Client sent AUTH, but no password is set
client = Redis(host="localhost", port=6379, db=0)

client.set("name", "Bob")
print(client.get("name"))
