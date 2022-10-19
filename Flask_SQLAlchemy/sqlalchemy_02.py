# 操作已有的数据库
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base


mysql_db = {
    'user': 'root',
    'passwd': '123456',
    'host': '127.0.0.1',
    'port': '3308'
}
# db_name = 'mysql+mysqlconnector://root:123456@localhost:3308/sqlalchemy_test'
db_name = f'mysql+pymysql://{mysql_db["user"]}:{mysql_db["passwd"]}@{mysql_db["host"]}:{mysql_db["port"]}/testemp'

engine = create_engine(db_name) # 连接数据库(创建连接池)
"""
#engine = create_engine(db_name, echo=True, pool_size=5, max_overflow=4, pool_recyle=7200, pool_timeout=30) # 连接数据库(创建连接池)
echo=True: 用于显示SQLAlchemy在操作数据库时所执行的SQL语句情况。简单来说, 如果其值为True,执行的SQL语句会在控制台被打印出来;如果其值为False, 则执行的SQL语句不在终端进行打印

pool_size: 连接池的大小, 默认值是5, 代表连接池本身可以创建的最大连接数。可根据实际情况进行调整。

max_overflow: 超过连接池大小以外最多可以创建的连接数, 默认值为10。当pool_size<连接数目<max_overflow时, 超过pool_size的部分可以正常练级恩访问。在使用过后, 超过部分不会放在连接池中, 而是被真正关闭。举个例子,  比如pool_size的值为5,  max_overflow的值为10,  连接数只要不大于5+10=15就可以。当连接数为8时, 拆过的3个连接使用过会被真正关闭。

pool_recyle: 连接重置周期, 默认为-1, 推荐设置为7200.即如果连接已空闲7200秒, 就自动重新获取, 以防止连接被关闭。

pool_timeout: 连接超时时间, 默认为30秒, 超过时间的连接都会连接失败。

?charset=utf8:对数据库进行编码设置, 能对数据库进行中文读写。如果不设置, 在进行数据添加、修改和更新时, 就会提示编码错误。
"""

# Base = automap_base()
# Base.prepare(engine, reflect=True)

# # 将已有数据库中的emp和dept分别映射到Emp和Dept类
# Emp = Base.classes.emp
# Dept = Base.classes.dept


Se = sessionmaker(bind=engine)  # 创建session访问数据库
session = Se()  # 实例化 (session 可类比 mysql.connector.connect.cursor() , 不同的是cursor执行的是sql语句, 还需要关闭)

sql = 'select * from emp;'

# session.execute(sql)
cur = engine.execute(sql)
print(cur.fetchall())
# session.query(Dept).all()

