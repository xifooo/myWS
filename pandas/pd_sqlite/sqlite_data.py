import sqlite3


conn = sqlite3.connect('stu.db')


def create_table():
    cursor = conn.cursor()
    
    table_sql = '''
    create table user(
        id integer primary key autoincrement not null,
        name text not null,
        age integer not null,
        score integer not null
    )
    '''
    cursor.execute(table_sql)
    conn.commit()
    
    
def insert_table():
    cursor = conn.cursor()
    
    sql_lst = [
        "insert into user(name, age, score)values('lili', 18, 560)",
        "insert into user(name, age, score)values('poly', 19, 600)",
        "insert into user(name, age, score)values('lilei', 30, 606)"
    ]
    for sql in sql_lst:
        cursor.execute(sql)
        conn.commit()
        
        
def select(table):
    sql = f'select * from {table}'
    # sql = 'select * from {table}'.format(table=table)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取全部数据
    for row in rows:
        print(row)


create_table()
insert_table()
select('user')