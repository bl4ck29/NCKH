from function.DataFunctions import DataFunctions
from datasource import Connection, DataFormater
from function import DataFunctions
import pandas

import datetime

conn = Connection.Connection(connectionString='mongodb+srv://bl4ck_29:Matkhau1234@cluster0.otjrb.azure.mongodb.net/test')
raw = conn.LoadData(col="DIT0230-1600796-HK1_2020-2021_20210304-1841", db="NCKH")
pdData = DataFormater.Convert(raw)
data = DataFunctions.DataFunctions(pdData)
data.pdData["ID"].unique().to
print(data.FindbyAttribute({"id":"187IT23616"}))