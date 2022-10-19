import sqlite3
import pandas as pd

from sqlite_data import select


conn = sqlite3.connect('stu.db')

data = [
    {'id': 4, 'name': '小明', 'age': 19, 'score': 590},
    {'id': 5, 'name': '小红', 'age': 20, 'score': 620},
    {'id': 6, 'name': '小红', 'age': 20, 'score': 620},
]

df = pd.DataFrame(data)
df.to_sql('student', con=conn, index=False, if_exists='fail')

select('student')