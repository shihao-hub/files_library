import pymongo
from pymongo.database import Database
from pymongo.collection import Collection


if __name__ == '__main__':
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    print(client)

    databases = client.list_database_names()
    print(databases)

    db = client.get_database("mail_app")
    users = db.get_collection("users")

    print(type(db))
    print(type(users))

    res = users.insert_one({
        "username": "smith"
    })
    print(res)

    res = users.insert_one({
        "username": "john"
    })
    print(res)

    res = users.find()
    print(res)
