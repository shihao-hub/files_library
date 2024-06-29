import sqlite3

conn = sqlite3.connect(r"E:\Edtior_Projects\PyCharmProjects\typeidea\typeidea\typeidea\db.sqlite3")
cursor = conn.cursor()
print(conn)
print(cursor)


cursor.execute("select * from blog_category;")
for e in cursor.fetchall():
    print(e)