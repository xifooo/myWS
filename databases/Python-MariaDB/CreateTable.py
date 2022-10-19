#!/usr/bin/python

import MySQLdb

# Open database connection
conn = MySQLdb.connect(
    host='3308',
    user='root',
    passwd='123456',
    db='emp'
    )  

# prepare a cursor object using cursor() method
cursor = conn.cursor()

# create a table
cursor.execute("DROP TABLE IF EXISTS MENU")
sql = """CREATE TABLE MENU (ORDERS  CHAR(20) NOT NULL)"""
cursor.execute(sql)

# disconnect from server
conn.close()