# import pymysql

# conn = pymysql.connect(host='localhost', db='INFORMATION', user='root', password='pass123#', charset='utf8', unix_socket="/var/lib/mysql/mysql.sock") 
# cursor = conn.cursor() 

# sql = '''CREATE TABLE FAL (
#     NO INT(255) NOT NULL,
#     NAME VARCHAR(25) NOT NULL,
#     AGE INT(11) NOT NULL,
#     TEXT VARCHAR(255) NOT NULL,
#     TIME DATETIME DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (NO)
# )'''


# sql1 = '''CREATE TABLE IMG (
#     NO INT(255) NOT NULL,
#     IMG1 VARCHAR(255) NOT NULL,
#     IMG2 VARCHAR(255) NOT NULL,
#     PRIMARY KEY (NO)
#     FOREIGN KEY (IMG1)

# )'''

# sql3 = '''CREATE TABLE IMG (
#     NO INT(255) NOT NULL,
#     URL VARCHAR(255) NOT NULL,
#     PRIMARY KEY (URL)
#     FOREIGN KEY (NO)
# )'''



# # sql = "create table 'FAL'(
# # NO VARCHAR NOT NULL(20),
# # NAME VARCHAR NOT NULL(25),
# # AGE INT,
# # TEXT VARCHAR(255) NOT NULL,
# # )"

# cursor.execute(sql) 
# cursor.execute(sql1)
# cursor.execute(sql2)
# conn.commit() 
# conn.close()