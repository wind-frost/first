WebSocket



'''

```
# websocket服务端
from dwebsocket.decorators import accept_websocket

conn = {}  # 连接池


@accept_websocket
def finish_order(request, name):
    if request.is_websocket:
        # 建立关联
        conn[name] = request.websocket

    for message in request.websocket:
        # 检测连接是否是正常状态
        pass


def send(request):
    # 支付宝已经支付成功，回调接口
    # 给商户发提醒
    name = 'admin'
    mes = json.dumps({'title': '你有新的订单了'}, ensure_ascii=False).encode('utf-8')
    conn[name].send(mes)
    return HttpResponse('ok')
```

'''

'''

```
from dwebsocket.decorators import accept_websocket
import json

# 存储连接websocket的用户
clients = {}

@accept_websocket
def websocketLink(request, username):
    # 获取连接
    if request.is_websocket:
        # 新增 用户  连接信息
        clients[username] = request.websocket
        # 监听接收客户端发送的消息 或者 客户端断开连接
        for message in request.websocket:
            break

 # 发送消息
def websocketMsg(client, msg):
    b1 = json.dumps(msg,ensure_ascii=False).encode('utf-8')
    client.send(b1)

# 服务端发送消息
def send(request):
    if clients:
        for i in clients:
             websocketMsg(clients['龙三'], {'title': '您有新的订单了'})
    return HttpResponse("ok")
```

'''

