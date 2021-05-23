from datetime import datetime
from pandas.core.indexing import IndexSlice
import ConnectToMongo
from functions import functions

connection = ConnectToMongo.connect("mongodb+srv://bl4ck_29:Matkhau1234@cluster0.otjrb.azure.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
lstCollections = connection.list("NCKH")
collection = connection.getData("NCKH", lstCollections[0], index=False)

func = functions.functions(collection)
data = func.limitbyTime([datetime(2021, 1, 1), datetime(2021, 1, 12)])