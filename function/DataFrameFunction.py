import pandas

def LimitByTime(data, startTime, endTime):
    return data.loc[(data["Time"]>=startTime) & (data["Time"]<=endTime)]

def FindByAttribute(data, dctQuery):
    condition = [True, True, True, True, True]
    if "id" in dctQuery:
        condition[0] = (data["ID"]== dctQuery["id"])
    if "name" in dctQuery:
        condition[1] =  (data["Name"]== str(dctQuery["name"]))
    if "event" in dctQuery:
        condition[2] =  (data["Event"]== str(dctQuery["event"]))
    if "component" in dctQuery:
        condition[3] =  (data["Component"]== str(dctQuery["component"]))
    if "Course" in dctQuery:
        condition[4] = (data["Course"] == str(dctQuery["Course"]))
    return data.loc[condition[0] & condition[1] & condition[2] & condition[3] & condition[4]]

def ListObjectName(data):
    return data.loc[(data["Type"]!="Forum") | (data["Type"]!="Label") | (data["Type"]!="Course")]["Course"].unique().tolist()

def listItem(data, colName):
    result = [item.replace(" ", "_") for item in data[colName].unique().tolist()]
    return result

def GroupByAttribute(data, lstAttr):
    return data.groupby(lstAttr)