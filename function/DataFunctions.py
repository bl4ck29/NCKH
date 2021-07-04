class DataFunctions:
    def __init__(self, pdData):
        self.pdData = pdData

    def Column(self):
        return list(self.pdData.columns)
    
    def LimitByTime(self, lstTime):
        return self.pdData.loc[(self.pdData["Time"] >= lstTime[0]) & (self.pdData["Time"] <= lstTime[1])]

    def FindbyAttribute(self, dctAttr):
        # Query pdData using pandas
        condition = [True, True, True, True]
        if "id" in dctAttr:
            condition[0] = (self.pdData["ID"]== dctAttr["id"])
        if "name" in dctAttr:
            condition[1] =  (self.pdData["Name"]== str(dctAttr["name"]))
        if "event" in dctAttr:
            condition[2] =  (self.pdData["Event name"]== str(dctAttr["event"]))
        if "component" in dctAttr:
            condition[3] =  (self.pdData["Component"]== str(dctAttr["component"]))
        return self.pdData.loc[condition[0] & condition[1] & condition[2] & condition[3]]

    def Score(self, standard=None):
        lstStudent = self.pdData.loc[self.pdData["ID"].notnull()]
        lstID = lstStudent["ID"].unique().tolist()
        result = {}
        for id in lstID:
            result[str(id)] = dict(self.pdData.loc[self.pdData["ID"] == id].groupby(["Event name"]).count()["Time"])
        for id, value in result.items():
            sumScore = 0
            for item, time in value.items():
                try:
                    time = int(time)
                    item = item.replace(" ", "_")
                    if item in standard:
                        score = standard[item]
                    else:
                        score = 1
                    sumScore += time * score
                except:
                    sumScore += 0
            result[id] = sumScore
        return result

    def ListItem(self, attr):
        return [item.replace(' ', '_') for item in self.pdData[attr].unique().tolist()]