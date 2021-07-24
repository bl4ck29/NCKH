from Cleansing import Cleansing
import Functions
import pandas, re

data = Cleansing(pandas.read_csv("D:/NCKH/Log files/DIT0090-05B0185-HK1_2020-2021_20210304-1826.csv", nrows=1000))
lstStd = Functions.ListItem(sample, "ID")

attrName = "Event context"
attrContent = "Course: Các nền tảng phát triển phần mềm _ 25T-IT"
sample = data.loc[(data["ID"].notnull()) & (data[attrName] ==  attContent)]

lstDone = Functions.ListItem(sample.loc[data[attrName]==attrContent], "ID")
lstNot = list(filter(lambda id: id not in lstDone, lstStd))

print(lstNot)