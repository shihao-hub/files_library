import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")

print(client)
# client["drafts"]
# db = client["test"]
# students = db["students"]
#
# students.update_one({"name": "Jordan"}, {"$set": {"gender": ["a"]}})

mail_app_db = client["mail_app"]
drafts_c = mail_app_db["drafts"]

count = drafts_c.count_documents({})
if count == 0:
    drafts_c.insert_one({
        "pk": 0,
        "data": [{
            "receivers": "1",
            "subject": "2",
            "body": "3"
        }]
    })
else:
    data_list = drafts_c.find_one({"pk": 0})["data"]
    data_list.append({
        "receivers": "1" * (count + 1),
        "subject": "2" * (count + 1),
        "body": "3" * (count + 1)

    })
    drafts_c.update_one({"pk": 0}, {
        "$set": {
            "data": data_list
        }
    })

    # if mongodb_db["drafts"] is None:
    #     mongodb_db["drafts"] = [data]
    # else:
    #     mongodb_db["drafts"].insert_one({
    #         "receivers": "111",
    #         "subject": "222",
    #         "body": "333"
    #     })
