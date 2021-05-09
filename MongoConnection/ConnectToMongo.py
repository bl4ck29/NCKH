import pymongo
def connect(connectString):
    connection = pymongo.MongoClient(connectString)
    database = connection["NCKH"]
    collection = database["res_logs"]
    return list(collection.find({}, {"_id":0}))