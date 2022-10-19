from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import os


app = Flask(__name__)

sqlite_db_addr = os.path.join(os.getcwd(),'flask_sqlalchemy_test.db')
# sqlite_db_addr = '/home/jyeho/sql/test.db'    # linux
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{sqlite_db_addr}' 

# mysql_db = {
#     'user' : 'root',
#     'passwd' : '123456',
#     'addr' : '127.0.0.1',
#     'port' : '3308',
# }
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_db["user"]}:{mysql_db["passwd"]}@{mysql_db["addr"]}:{mysql_db["port"]}/test'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 密钥
app.config['SECRET_KEY'] = 'shenmedouxing'

# 实例化一个数据库实例
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'student'
    s_id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(64), nullable=False, default='')
    s_gender = db.Column(db.Enum('男','女'), nullable=False)
    s_phone = db.Column(db.String(11))
    
# class Score(db.Model):
#     __tablename__ = 'score'
#     id = db.Column(db.Integer, primary_key=True)
#     s_id = 
#     s_score = 
#     c_name = db.Column(db.String(64), nullable=False)
    
class Course(db.Model):
    __tablename__ = 'course'
    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(64), nullable=False)
    
class Teacher(db.Model):
    __tablename__ = 'teacher'
    t_id = db.Column(db.Integer, primary_key=True)
    t_name = db.Column(db.String(64), nullable=False)
    t_gender = db.Column(db.Enum('男','女'), nullable=False)
    t_phone = db.Column(db.String(11))
    
if __name__ == '__main__':
    db.create_all()