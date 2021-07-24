def LimitByTime(data, lstTime):
    return data.loc[(data["Time"]>=lstTime[0]) & (data["Time"]<=lstTime[1])]

def IdNotnull(data):
    return data.loc[data["ID"].notnull()]

def IdNull(data):
    return data.loc[data["ID"].isnull()]

def FindByAttribute(data, dctAttr):
    condition = [True, True, True, True]
    if "id" in dctAttr:
        condition[0] = (data["ID"]== dctAttr["id"])
    if "name" in dctAttr:
        condition[1] =  (data["Name"]== str(dctAttr["name"]))
    if "event" in dctAttr:
        condition[2] =  (data["Event name"]== str(dctAttr["event"]))
    if "component" in dctAttr:
        condition[3] =  (data["Component"]== str(dctAttr["component"]))
    return data.loc[condition[0] & condition[1] & condition[2] & condition[3]]

def ListItem(data, attr, outCol=[]):
    if outCol == []:
        return data[attr].unique().tolist()