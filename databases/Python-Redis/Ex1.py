import redis, threading

def connect():
    """
    获取 Redis 连接
    :return: Redis Client
    """
    pool = redis.ConnectionPool(
        host = '39.96.215.69',
        port = 6379,
        db = 14,
        password = "qwer1011",
        socket_timeout = None,
        socket_connect_timeout = None
    )
    return redis.Redis(connection_pool=pool)

redis.set("a", "b")
_str = redis.get('a')
redis.delete("a")