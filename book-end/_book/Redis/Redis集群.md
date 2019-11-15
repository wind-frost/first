 redis cluster 是redis官方提供的分布式解决方案，在3.0版本后推出的，有效地解决了redis分布式的需求，当一个redis节点挂了可以快速的切换到另一个节点。当遇到单机内存、并发等瓶颈时，可以采用分布式方案要解决问题。 

## Redis Cluster（Redis集群）简介



redis是一个开源的key value存储系统，受到了广大互联网公司的青睐。redis3.0版本之前只支持单例模式，在3.0版本及以后才支持集群，我这里用的是redis3.0.0版本；
redis集群采用P2P模式，是完全去中心化的，不存在中心节点或者代理节点；
redis集群是没有统一的入口的，客户端（client）连接集群的时候连接集群中的任意节点（node）即可，集群内部的节点是相互通信的（PING-PONG机制），每个节点都是一个redis实例；
为了实现集群的高可用，即判断节点是否健康（能否正常使用），redis-cluster有这么一个投票容错机制：如果集群中超过半数的节点投票认为某个节点挂了，那么这个节点就挂了（fail）。这是判断节点是否挂了的方法；
那么如何判断集群是否挂了呢? -> 如果集群中任意一个节点挂了，而且该节点没有从节点（备份节点），那么这个集群就挂了。这是判断集群是否挂了的方法；
那么为什么任意一个节点挂了（没有从节点）这个集群就挂了呢？-> 因为集群内置了16384个slot（哈希槽），并且把所有的物理节点映射到了这16384[0-16383]个slot上，或者说把这些slot均等的分配给了各个节点。当需要在Redis集群存放一个数据（key-value）时，redis会先对这个key进行crc16算法，然后得到一个结果。再把这个结果对16384进行求余，这个余数会对应[0-16383]其中一个槽，进而决定key-value存储到哪个节点中。所以一旦某个节点挂了，该节点对应的slot就无法使用，那么就会导致集群无法正常工作。
综上所述，每个Redis集群理论上最多可以有16384个节点。



[Redis集群详解]( https://blog.csdn.net/miss1181248983/article/details/90056960 )

## 集群模式 



```
* 主从模式
* Sentinel模式
* Cluster模式
```

## 主从模式介绍

主从模式是三种模式中最简单的，在主从复制中，数据库分为两类：主数据库(master)和从数据库(slave)。

其中主从复制有如下特点：

> * 主数据库可以进行读写操作，当读写操作导致数据变化时会自动将数据同步给从数据库
> * 从数据库一般都是只读的，并且接收主数据库同步过来的数据
> * 一个master可以拥有多个slave，但是一个slave只能对应一个master
> * slave挂了不影响其他slave的读和master的读和写，重新启动后会将数据从master同步过来
> * master挂了以后，不影响slave的读，但redis不再提供写服务，master重启后redis将重新对外提供写服务
> * master挂了以后，不会在slave节点中重新选一个master

工作机制：

> 当slave启动后，主动向master发送SYNC命令。master接收到SYNC命令后在后台保存快照（RDB持久化）和缓存保存快照这段时间的命令，然后将保存的快照文件和缓存的命令发送给slave。slave接收到快照文件和命令后加载快照文件和缓存的执行命令。
>
> 复制初始化后，master每次接收到的写命令都会同步发送给slave，保证主从数据一致性。
>

安全设置：

当master节点设置密码后，

> 客户端访问master需要密码
>
> 启动slave需要密码，在配置文件中配置即可
>
> 客户端访问slave不需要密码

缺点：

> 从上面可以看出，master节点在主从模式中唯一，若master挂掉，则redis无法对外提供写服务。
>
>  可以看到，在master节点写入的数据，很快就同步到slave节点上，而且在slave节点上无法写入数据。 
>



## Sentinel模式介绍

主从模式的弊端就是不具备高可用性，当master挂掉以后，Redis将不能再对外提供写入操作，因此sentinel应运而生。

sentinel中文含义为哨兵，顾名思义，它的作用就是监控redis集群的运行状况，特点如下：

> * sentinel模式是建立在主从模式的基础上，如果只有一个Redis节点，sentinel就没有任何意义
>
> * 当master挂了以后，sentinel会在slave中选择一个做为master，并修改它们的配置文件，其他slave的配置文件也会被修改，比如slaveof属性会指向新的master
>
> * 当master重新启动后，它将不再是master而是做为slave接收新的master的同步数据
>
> * sentinel因为也是一个进程有挂掉的可能，所以sentinel也会启动多个形成一个sentinel集群
>
> * 多sentinel配置的时候，sentinel之间也会自动监控
>
> * 当主从模式配置密码时，sentinel也会同步将配置信息修改到配置文件中，不需要担心
>
> * 一个sentinel或sentinel集群可以管理多个主从Redis，多个sentinel也可以监控同一个redis
>
> * sentinel最好不要和Redis部署在同一台机器，不然Redis的服务器挂了以后，sentinel也挂了

 工作机制： 

> * 每个sentinel以每秒钟一次的频率向它所知的master，slave以及其他sentinel实例发送一个 PING 命令 
> * 如果一个实例距离最后一次有效回复 PING 命令的时间超过 down-after-milliseconds 选项所指定的值， 则这个实例会被sentinel标记为主观下线。 
> * 如果一个master被标记为主观下线，则正在监视这个master的所有sentinel要以每秒一次的频率确认master的确进入了主观下线状态
> * 当有足够数量的sentinel（大于等于配置文件指定的值）在指定的时间范围内确认master的确进入了主观下线状态， 则master会被标记为客观下线 
> * 在一般情况下， 每个sentinel会以每 10 秒一次的频率向它已知的所有master，slave发送 INFO 命令 
> * 当master被sentinel标记为客观下线时，sentinel向下线的master的所有slave发送 INFO 命令的频率会从 10 秒一次改为 1 秒一次 
> * 若没有足够数量的sentinel同意master已经下线，master的客观下线状态就会被移除；
> * 若master重新向sentinel的 PING 命令返回有效回复，master的主观下线状态就会被移除

当使用sentinel模式的时候，客户端就不要直接连接Redis，而是连接sentinel的ip和port，由sentinel来提供具体的可提供服务的Redis实现，这样当master节点挂掉以后，sentinel就会感知并将新的master节点提供给使用者。 



## Cluster模式介绍

sentinel模式基本可以满足一般生产的需求，具备高可用性。但是当数据量过大到一台服务器存放不下的情况时，主从模式或sentinel模式就不能满足需求了，这个时候需要对存储的数据进行分片，将数据存储到多个Redis实例中。cluster模式的出现就是为了解决单机Redis容量有限的问题，将Redis的数据根据一定的规则分配到多台机器。

cluster可以说是sentinel和主从模式的结合体，通过cluster可以实现主从和master重选功能，所以如果配置两个副本三个分片的话，就需要六个Redis实例。因为Redis的数据是根据一定规则分配到cluster的不同机器的，当数据量过大时，可以新增机器进行扩容。

使用集群，只需要将redis配置文件中的cluster-enable配置打开即可。每个集群中至少需要三个主数据库才能正常运行，新增节点非常方便。

cluster集群特点：

> * 多个redis节点网络互联，数据共享
>
> * 所有的节点都是一主一从（也可以是一主多从），其中从不提供服务，仅作为备用
>
> * 不支持同时处理多个key（如MSET/MGET），因为redis需要把key均匀分布在各个节点上，
>   并发量很高的情况下同时创建key-value会降低性能并导致不可预测的行为
>   
> * 支持在线增加、删除节点
>
> * 客户端可以连接任何一个主节点进行读写





参考博客：

[Docker搭建Redis一主两从三哨兵]( https://www.cnblogs.com/fan-gx/p/11463400.html )  

[[redis主从复制下哨兵模式---选举原理](https://www.cnblogs.com/huangfuyuan/p/9880379.html)

[Redis哨兵机制原理](https://www.cnblogs.com/Eugene-Jin/p/10819601.html)

 [Redis集群常用命令](https://www.cnblogs.com/gossip/p/5993922.html) 