from pandas.io import sql
import sqlite3


conn = sqlite3.connect('stu.db')
query = 'select * from user;'

results = sql.read_sql(query, con=conn)
print(results.head())