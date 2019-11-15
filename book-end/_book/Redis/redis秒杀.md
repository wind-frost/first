setnx秒杀

```python
redis_client = get_redis_connection('online')
#获取一个锁
# lock_name：锁定名称
# acquire_time: 客户端等待获取锁的时间
# time_out: 锁的超时时间
def acquire_lock(lock_name, acquire_time=10, time_out=10):
    """获取一个分布式锁,其实就是给锁设置一个超时时间并返回一个锁的标识"""
    identifier = str(uuid.uuid4())
    # 获取锁的结束时间
    end = time.time() + acquire_time
    # 锁的名称
    lock = "string:lock:" + lock_name
    while time.time() < end:
        if redis_client.setnx(lock, identifier):
            # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
            redis_client.expire(lock, time_out)
            return identifier
        # 判断当前锁是否还存在过期时间, ttl返回剩余的过期时间
        elif not redis_client.ttl(lock):
            redis_client.expire(lock, time_out)
        time.sleep(0.001)
    return False


#释放一个锁
def release_lock(lock_name, identifier):
    """通用的锁释放函数"""
    lock = "string:lock:" + lock_name
    # 开启一个队列
    pip = redis_client.pipeline(True)
    while True:
        try:
            # 对lock这个锁进行监听
            pip.watch(lock)
            lock_value = redis_client.get(lock)
            if not lock_value:
                return True
            if lock_value.decode() == identifier:
                print('查看标识', lock_value.decode())
                # 标记一个事务块的开始,事务内的命令会放在队列中
                pip.multi()
                # 删除锁
                pip.delete(lock)
                # 最后有execute触发执行事务
                pip.execute()
                return True
            # 取消监听
            pip.unwatch()
            # 退出
            break
        except:
        # except redis.excetions.WacthcError:
            pass
    return False



def seckill(one_buy):
    identifier=acquire_lock('resource')
    if identifier:
        time.sleep(1)
        if one_buy['count']<1:
            print("没抢到，产品没有了")
            release_lock('resource', identifier)
            return False
        else:
            one_buy['count'] -= 1
            redis_client.hset('course' + str(datetime.now())[:10],
                              str(one_buy['act']) + ',' + str(one_buy['time']) + ',' + str(one_buy['course']),
                              json.dumps(one_buy))
            print("抢到一个产品，还剩%d张票" % one_buy['count'])
            release_lock('resource', identifier)
            return True
    else:
        return False
```



redis队列秒杀

```python
# 循环向队列内添加数量
for i in range(int(one.count)):
	conn.lpush(one.id, 1)
	conn.expire(one.id, 300)

# 弹出队列内的元素
ret = conn.lpop(course_id)
	print(ret)
```

