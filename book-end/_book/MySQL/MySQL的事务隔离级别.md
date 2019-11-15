MySQL的事务隔离级别



MySQL事务（ACID）的特点：

- 原子性 (atomicity)

 - 一致性(consistency)
 - 隔离性(isolation)
 - 持久性(durability)



在SQL标准中定义了四种隔离级别，每一种级别都规定了一个事务所做的修改，那些在事务内和事物间是可见的，那些是不可见的。

较低级别的隔离通常可以执行更高的并发，系统的开销也更低。



READ UNCOMMITTED (未提交读)   read uncommitted

READ COMMITTED(提交读)              read committed

REPEATABLE READ(可重复度)           repeatable read   (默认)  脏读

SERIALIZABLE(可串行化)                    serializable



