from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


mysql_db = {
    'user': 'root',
    'passwd': '123456',
    'host': '127.0.0.1',
    'port': '3308'
}

# db_name = 'mysql+mysqlconnector://root:123456@localhost:3308/sqlalchemy_test'
db_name = f'mysql+pymysql://{mysql_db["user"]}:{mysql_db["passwd"]}@{mysql_db["host"]}:{mysql_db["port"]}/sqlalchemy_t'

Base = declarative_base()   # 1、构造 declarative_base
class User(Base):   # 1.1 继承Base ———— 创建表结构，或者叫 model
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    
engine = create_engine(db_name) # 2、连接数据库(创建连接池)
Base.metadata.create_all(engine)    # 2.1 建表

Se = sessionmaker(bind=engine)  # 3、创建session访问数据库
session = Se()  # (session 可类比 mysql.connector.connect.cursor() , 不同的是cursor执行的是sql语句, 还需要关闭)
