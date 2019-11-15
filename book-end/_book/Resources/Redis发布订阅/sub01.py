import redis

conn = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

# 第一步 生成一个订阅者对象
pubsub = conn.pubsub()

# 第二步 订阅一个消息

pubsub.subscribe("News333")

# 创建一个接收
print('pub01')
while True:
    print("working~~~")
    msg = pubsub.parse_response()
    print(msg)
