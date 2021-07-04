from os import path
import pymongo

class Connection:
    def __init__(self, connectionString=False, pathFile=False):
        if connectionString and not pathFile:
            self.data = pymongo.MongoClient(connectionString)
            self.connectMethod = "connectionString"
        elif pathFile and not connectionString:
            self.data = open(pathFile, encoding="UTF-8")
            self.connectMethod = "pathFile"
        else:
            raise ("Please select one way")
    
    def List(self):
        if self.connectMethod == "connectionString":
            lstDB = self.data.list_database_names()
            result = {}
            for db in lstDB:
                result[db] = self.data[db].list_collection_names()
            return result
        else:
            raise "Connection is not provding list method"

    def LoadData(self, col=None, db="NCKH"):
        if self.connectMethod == "connectionString":
            return self.data[db][col].find({}, {"_id":0})
        if self.connectMethod == "pathFile":
            return self.data.read()