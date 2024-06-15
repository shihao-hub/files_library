import traceback

import pymysql

db = pymysql.connect(user="root", password="zsh20010417", host="127.0.0.1", port=3306, database="course")

cursor = db.cursor()

try:
    res = cursor.execute("insert intocustomers(cust_name) values(10001)")
    print(res)
    # db.commit()
except Exception as e:
    print(traceback.format_exc())
    db.close()
