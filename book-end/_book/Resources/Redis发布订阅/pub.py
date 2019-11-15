import redis

conn = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

conn.publish("News333", "News333:1998")
conn.publish("News666", "News666:1998")
conn.publish("News999", "News999:1998")
conn.publish("News01", "News01:1998")
