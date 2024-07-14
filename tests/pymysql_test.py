import traceback

import pymysql

db = pymysql.connect(user="root", password="zsh20010417", host="127.0.0.1", port=3306, database="course")

cursor = db.cursor()
try:
    res = cursor.execute("show databases;")
    # res = cursor.execute("insert into customers(cust_name) values(10006)")
    for e in cursor.fetchall():
        print(e)
except pymysql.err.ProgrammingError as e:
    print(traceback.format_exc())
else:
    db.commit()
finally:
    db.close()
