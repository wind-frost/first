import redis

conn = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

# 第一步 生成一个订阅者对象
pubsub = conn.pubsub()

# 第二步 订阅一个消息

# pubsub.subscribe("News333")
pubsub.subscribe("News01")
# pubsub.psubscribe('News666','News333') # 批量订阅频道
pubsub.psubscribe('News*')  # 订阅以News开头的所有 频道
# pubsub.unsubscribe('News01') # 退订

# 创建一个接收
print('pub02')
while True:
    print("working~~~")
    msg = pubsub.parse_response()
    print(msg)
