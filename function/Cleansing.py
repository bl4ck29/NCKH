import pandas, re

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
    TIME = row["Time"].to_pydatetime()
    course = row["Event context"]
    try:
        TYPE = course[ : course.index(":")]
        COURSE = course[course.index(" ")+1 : ]
    except:
        TYPE = None
        COURSE = None
    COMPONENT = row["Component"]
    EVENT = row["Event name"]
    return (TIME, ID, NAME, TYPE, COURSE, COMPONENT, EVENT)