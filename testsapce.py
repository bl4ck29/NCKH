from datasource import Connection, DataFormater
from function import Functions
import pandas, re, datetime

data = Connection.Connection(pathFile="D:/NCKH/Log files/DIT0090-05B0185-HK1_2020-2021_20210304-1826.csv")
data = DataFormater.Cleansing(DataFormater.Convert(data))
print(data.columns)