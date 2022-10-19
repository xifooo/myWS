import orm, asyncio
from models import User, Blog, Comment

async def test(loop):
    await orm.create_pool(loop=loop, user='root', password='123456', db='awesome')
    u = User(name='Test', email='test@gmail.com', passwd='123456789', image='')
    await u.save()
    # 添加到数据库后要关闭连接池, 否则报错 RuntimeError: Event loop is closed
    orm.__pool.close()
    await orm.__pool.wait_closed()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    loop.close()