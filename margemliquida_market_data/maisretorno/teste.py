import redis

r = redis.Redis(
    host="redis-18360.c53.west-us.azure.cloud.redislabs.com",
    port=18360,
    password="LYNMWXMrqS9o4griad4afTOAvXBbiD0D",
    decode_responses=True,
)

r.set("bdrs", str(["1", "2", "3"]))
print(r.get("bdrs"))
