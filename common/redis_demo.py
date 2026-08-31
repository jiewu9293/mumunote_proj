import redis
# 不推荐这么写
# red = redis.Redis(host='192.168.1.129',port=6379,db=1)

# 使用连接池的方式进行连接，这样它就会对我们的连接进行一个管理
# 推荐这么写
# decode_responses 这个参数如果不加，下边就给你返回bytes，需要转换才能看到中文
pool = redis.ConnectionPool(host='127.0.0.1',port=6379,db=1,decode_responses=True)

redis_client = redis.Redis(connection_pool=pool)
# 字符串类型的处理
redis_client.set("name","大周老师")  # 单独设置一个值
print(redis_client.get("name"))

redis_client.mset({"age":18,"address":"北京"})
print(redis_client.mget("name","age","address"))  # 我们同时获取多个值的时候，这里返回的是列表类型
print(redis_client.exists("name"))  # 存在是1，不存在是0
print(redis_client.exists("myname"))


print(redis_client.get("myname"))
print(redis_client.dbsize())
print(redis_client.lastsave())

#==========================hash类型操作===========================
# 新增一个
redis_client.hset(name="userHash",key="username",value="dazhoulaoshi")
# 新增多个
redis_client.hset(name="userHash2",mapping={"username":"大周老师",
                                            "password":"123456",
                                            "nickname":"大大",
                                            "address":"北京"})

print(redis_client.hget("userHash2","username"))
print(redis_client.hgetall("userHash2"))
#==========================list类型、set操作===========================
redis_client.rpush("numberRight",1,2,3,4,5,6)
redis_client.lpush("numberLeft",1,2,3,4,5,6)

# 这里越打印越长，是因为每一次我们运行代码的时候都会往numberRight里边重新放1到6
for i in range(redis_client.llen("numberRight")):
    print(redis_client.lindex("numberRight",i))
redis_client.sadd("setNum",11,12,13,14)
set_number = redis_client.smembers("setNum")
print(set_number)
for i in set_number:
    print(i)

#==========================zset操作===========================
redis_client.zadd("myzset",{"v1":40,"v2":20,"v3":30})
#查询分数在 20～30 之间的成员：
r = redis_client.zrangebyscore("myzset",20,30)
print(r)
#加上 withscores=True 会同时返回成员和分数
r = redis_client.zrangebyscore("myzset",20,30,withscores=True)
print(r)
# 差具体成员的索引值，或者叫排名也行
print(redis_client.zrank("myzset","v1"))
