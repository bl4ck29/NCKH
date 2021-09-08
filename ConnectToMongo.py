import pymongo
class connect:
    def __init__(self, connectString):
        self.connection = pymongo.MongoClient(connectString)

    def List(self, dbName=None):
        result = self.connection.list_database_names()
        if dbName in result:
            return self.connection[dbName].list_collection_names()
        return result
    
    def GetData(self, dbName, colName, index=True):
        collection = self.connection[dbName][colName]
        if index:
            return collection.find({})
        else:
            return collection.find({}, {"_id":0})