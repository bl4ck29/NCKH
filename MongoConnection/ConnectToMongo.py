import pymongo
class Connect:
    def __init__(self, connectString, db, col):
        self.connection = pymongo.MongoClient(connectString)
        self.__database = db
        self.__collection = col
        
    def connect(self, index=True):
        collection = self.connection[self.__database][self.__collection]
        if index:
            return list(collection.find({}))
        else:
            return list(collection.find({}, {"_id":0}))

    def list(self):
        dct = {}
        db = self.connection.list_database_names()
        for i in db:
            dct[i] = self.connection[i].list_collection_names()
        return dct

    def disconnect(self):
        del(self.connection)