# Script to ccreate drop Database Table
import sqlite3


conn = sqlite3.connect('tgif.db')
print ("Opened database successfully")


# conn.execute('DROP TABLE tgif')
# print ("Table Deleted successfully")
conn.execute('CREATE TABLE tgif (sno INTEGER  NOT NULL PRIMARY KEY, nameofemployee TEXT NOT NULL, amount INTEGER NOT NULL, desc TEXT NOT NULL, date_created timestamp)')
print ("Table created successfully")
conn.close()