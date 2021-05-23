import pymongo
class connect:
    def __init__(self, connectString):
        self.connection = pymongo.MongoClient(connectString)

    def list(self, dbName=None):
        dct = {}
        db = self.connection.list_database_names()
        for i in db:
            dct[i] = self.connection[i].list_collection_names()
        if dbName in dct:
            return dct[dbName]
        return dct

    def getData(self, dbName, colName, index=True):
        collection = self.connection[dbName][colName]
        if index:
            return collection.find({})
        else:
            return collection.find({}, {"_id":0})