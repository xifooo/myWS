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

# Prepare SQL query to INSERT a record into the database.
sql = """INSERT INTO MENU(ORDERS) VALUES ('O1')"""

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   conn.commit()
except:
   # Rollback in case there is any error
   conn.rollback()

# disconnect from server
conn.close()