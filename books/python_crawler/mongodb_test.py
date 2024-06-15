import pprint
import sys
import traceback
from collections.abc import Iterable

import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

client = pymongo.MongoClient(host="localhost", port=27017)
# client = pymongo.MongoClient("mongodb://localhost:27017")

# pprint.pprint(client.__dict__)

try:
    databases = client.list_database_names()
    print(databases)

    db: Database = client.test
    collection: Collection = db.students

    print(type(db))
    print(type(collection))

    res = collection.insert_one({
        "id": "202406100001",
        "name": "Jordan",
        "age": 20,
        "gender": "male"
    })
    print(res)
    print(client.list_database_names())
    print(collection.find_one({"id": "202406100001"}))
except Exception as e:
    # sys.stderr.write(traceback.format_exc())
    # sys.stderr.write("\n")
    print(traceback.format_exc())
    client.close()
