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


sql = "SELECT * FROM MENU"

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      orders = row[0]
      # Now print fetched result
      print ("%s" %orders)

except:
   # Rollback in case there is any error
   print ('unable to fetch data')

# disconnect from server
conn.close()