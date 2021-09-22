import mysql.connector, os, pandas, configparser
from Cleansing import Cleansing

PATH = "/home/vlu-fit/RawLogFiles"
os.chdir(PATH)

parser = configparser.ConfigParser("config.cfg")

config = {"host":parser.get("mysql", "host"), "user":parser.get("mysql", "user"), "password":parser.get("mysql", "password"), "database":parser.get("mysql", "database"), "connect_timeout":int(parser.get("mysql", "connect_timeout"))}

connection = mysql.connector.connect(**config)
cursor = connection.cursor()

LISTFILE = os.listdir()
for name in LISTFILE:
    data = pandas.read_csv(PATH + name).astype({"Time":"datetime64"})
    FILENAME = name.replace("-", "_").replace(".csv", "")

    queryCreateTable = "create table " + FILENAME + " (Time datetime, ID char(10), Name varchar(50), Type char(30), Course test, Component char(50), Event text"
    cursor.execute(queryCreateTable)
    connection.commit()

    queryInsert = "insert into LogFile."+FILENAME+"(Time, ID, Name, Type, Course, Component, Event) values (%s, %s, %s, %s, %s, %s, %s);"
    for i in range(len(data)):
        row = data.loc[i]
        result = Cleansing(row)
        cursor.execute(queryInsert, result)
        connection.commit()
    print(name + "- DONE")
cursor.close()
connection.close()
