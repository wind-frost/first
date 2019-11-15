[Redis常用数据类型及使用场景](https://www.cnblogs.com/tqlin/p/10478459.html)参考博客

Sorted-set（有序的set集合）

> 与Redis集合类似，Redis排序集是字符串的非重复集合。不同之处在于，排序集的每个成员都与分数相关，分数是用来对排序集进行排序的，从最小的分数到最大的分数。虽然成员是唯一的，分数可以重复。使用排序的集合，可以以一种非常快的方式(在与元素数量的对数成比例的时间内)添加、删除或更新元素。可以非常快速地按分数或按级别(位置)获取范围。访问排序集的中间也非常快，所以可以使用排序集作为一个非重复元素的智能列表，在其中你可以快速访问所需的一切:元素顺序，快速存在测试，快速访问中间元素!简而言之，使用排序集，你可以完成许多性能优异的任务，这些任务在其他类型的数据库中很难建模。

有了排序集，你可以:

> - 在一款大型在线游戏中，你可以选择一个排行榜，每当有新的分数被提交时，你就可以使用ZADD进行更新。可以轻松地使用ZRANGE获取顶级用户，还可以在给定用户名的情况下，使用ZRANK返回其在列表中的排名。同时使用ZRANK和ZRANGE，可以向用户显示与给定用户类似的分数。这些操作都非常快。
> - 排序集通常用于索引存储在Redis中的数据。例如，如果有许多表示用户的散列，那么可以使用一个已排序的集合，其中的元素以用户的年龄为得分，以用户的ID为值。因此，使用ZRANGEBYSCORE检索给定时间间隔的所有用户既简单又快速。
> - 排序集可能是最先进的Redis数据类型，所以花点时间检查排序集命令的完整列表，以发现可以使用Redis做什么!



## 存取

```
# 存
ZADD key 排序 value
# 取
ZRANGE key start stop
```

### Redis 有序集合命令

下表列出了 redis 有序集合的基本命令:

| 序号 | 命令及描述                                                   |
| :--- | :----------------------------------------------------------- |
| 1    | [ZADD key score1 member1 [score2 member2\]](https://www.runoob.com/redis/sorted-sets-zadd.html) 向有序集合添加一个或多个成员，或者更新已存在成员的分数 |
| 2    | [ZCARD key](https://www.runoob.com/redis/sorted-sets-zcard.html) 获取有序集合的成员数 |
| 3    | [ZCOUNT key min max](https://www.runoob.com/redis/sorted-sets-zcount.html) 计算在有序集合中指定区间分数的成员数 |
| 4    | [ZINCRBY key increment member](https://www.runoob.com/redis/sorted-sets-zincrby.html) 有序集合中对指定成员的分数加上增量 increment |
| 5    | [ZINTERSTORE destination numkeys key [key ...\]](https://www.runoob.com/redis/sorted-sets-zinterstore.html) 计算给定的一个或多个有序集的交集并将结果集存储在新的有序集合 key 中 |
| 6    | [ZLEXCOUNT key min max](https://www.runoob.com/redis/sorted-sets-zlexcount.html) 在有序集合中计算指定字典区间内成员数量 |
| 7    | [ZRANGE key start stop [WITHSCORES\]](https://www.runoob.com/redis/sorted-sets-zrange.html) 通过索引区间返回有序集合指定区间内的成员 |
| 8    | [ZRANGEBYLEX key min max [LIMIT offset count\]](https://www.runoob.com/redis/sorted-sets-zrangebylex.html) 通过字典区间返回有序集合的成员 |
| 9    | [ZRANGEBYSCORE key min max [WITHSCORES\] [LIMIT]](https://www.runoob.com/redis/sorted-sets-zrangebyscore.html) 通过分数返回有序集合指定区间内的成员 |
| 10   | [ZRANK key member](https://www.runoob.com/redis/sorted-sets-zrank.html) 返回有序集合中指定成员的索引 |
| 11   | [ZREM key member [member ...\]](https://www.runoob.com/redis/sorted-sets-zrem.html) 移除有序集合中的一个或多个成员 |
| 12   | [ZREMRANGEBYLEX key min max](https://www.runoob.com/redis/sorted-sets-zremrangebylex.html) 移除有序集合中给定的字典区间的所有成员 |
| 13   | [ZREMRANGEBYRANK key start stop](https://www.runoob.com/redis/sorted-sets-zremrangebyrank.html) 移除有序集合中给定的排名区间的所有成员 |
| 14   | [ZREMRANGEBYSCORE key min max](https://www.runoob.com/redis/sorted-sets-zremrangebyscore.html) 移除有序集合中给定的分数区间的所有成员 |
| 15   | [ZREVRANGE key start stop [WITHSCORES\]](https://www.runoob.com/redis/sorted-sets-zrevrange.html) 返回有序集中指定区间内的成员，通过索引，分数从高到低 |
| 16   | [ZREVRANGEBYSCORE key max min [WITHSCORES\]](https://www.runoob.com/redis/sorted-sets-zrevrangebyscore.html) 返回有序集中指定分数区间内的成员，分数从高到低排序 |
| 17   | [ZREVRANK key member](https://www.runoob.com/redis/sorted-sets-zrevrank.html) 返回有序集合中指定成员的排名，有序集成员按分数值递减(从大到小)排序 |
| 18   | [ZSCORE key member](https://www.runoob.com/redis/sorted-sets-zscore.html) 返回有序集中，成员的分数值 |
| 19   | [ZUNIONSTORE destination numkeys key [key ...\]](https://www.runoob.com/redis/sorted-sets-zunionstore.html) 计算给定的一个或多个有序集的并集，并存储在新的 key 中 |
| 20   | [ZSCAN key cursor [MATCH pattern\] [COUNT count]](https://www.runoob.com/redis/sorted-sets-zscan.html) 迭代有序集合中的元素（包括元素成员和元素分值） |

