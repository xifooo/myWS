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

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)

# disconnect from server
conn.close()