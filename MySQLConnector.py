import pandas, re, os, mysql.connector, datetime

def SplitNameAndId(string):
    ID, NAME = '', ''
    
    PATTERN = '[0-9]+[A-Z]+[0-9]+'
    
    lstNameAndID = string.split('-')
    match = re.search(PATTERN, string)
    if match:
        ID = match.group()
        if len(lstNameAndID) <3:
            start = string.index(' ') + 1
            end = string.rindex(' ')
            NAME = str(string[start : end])
        else:
            NAME = str(lstNameAndID[1]).strip()
    else:
        NAME = str(string)
    return ID, NAME

def Cleansing(row):
    ID, NAME = SplitNameAndId(row["User full name"])
    TIME = row["Time"]
    COURSE = row["Event context"].replace('Course: ', '')
    COMPONENT = row["Component"]
    EVENT = row["Event name"]
    return (TIME, ID, NAME, COURSE, COMPONENT, EVENT)



config = {"host":"localhost", "user":"root", "password":"Matkhau@1234", "database":"LogFiles"}
connection = mysql.connector.connect(**config)
cursor = connection.cursor()

PATH = "/home/bl4ck29/Downloads/RawLogFiles/"

LISTFILE = os.listdir()
for name in LISTFILE:
    data = pandas.read_csv(PATH + name).astype({"Time":"datetime64"})
    
    FILENAME = name.replace("-", "_").replace(".csv", "")
    
    queryCreateTable = "create table " + FILENAME + " (Time timestamp, ID char(10), Name varchar(50), Course text, Component char(20), Event text)"
    cursor.execute(queryCreateTable)
    connection.commit()
    
    queryInsert = "insert into "+ FILENAME + " (Time, ID, Name, Course, Component, Event) values (%s, %s, %s, %s, %s, %s)"
    for i in range(len(data)):
        row = data.loc[i]
        result = Cleansing(row)
        cursor.execute(queryInsert, result)
        connection.commit()
cursor.close()
connection.close()