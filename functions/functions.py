import pandas, re, datetime, json

class functions():
    def __init__(self, data):
        self.data = pandas.DataFrame(data)
        self.data = self.data.astype({"Time" : "datetime64"})
        
    def cleansing(self):
        columns = list(self.data.columns)
        pat_id = '[0-9]+[A-Z]+[0-9]+'
        # Handle the empty row in USER FULL NAME
        self.data.loc[self.data["User full name"]=="-", "User full name"] = "Admin"
        for row in range(len(self.data)):
            # Split the time and date from TIME field
            text = str(self.data.iloc[row, columns.index('Time')]).split(',')
            date = text[0].split("/")
            time = text[1].split(":")
            self.data.loc[row, "Time"] = datetime.datetime(
                datetime.date.today().year, int(date[1].strip()), int(date[0].strip()), int(time[0].strip()), int(time[1].strip())
                )
            # Search for the student' ID
            name = self.data.iloc[row, columns.index('User full name')]
            lst = name.split("-")
            match = re.search(pat_id, name)
            if match:
                self.data.loc[row, "ID"] = match.group()
                # Space instead of - in name
                if len(lst) < 3:
                    start = name.index(" ")
                    end = name.rindex(" ")
                    self.data.loc[row, "Name"] = str(name[start : end].strip())
                else:
                    self.data.loc[row, "Name"] = str(lst[1].strip())
            else:
                self.data.loc[row, "ID"] = pandas.NaT
                self.data.loc[row, "Name"] = str(name)

            if self.data.loc[row, "Component"] == "Assignment":
                self.data.loc[row, "Object"] = str(self.data.loc[row, "Event context"]).split("-")[-1]
            else:
                self.data.loc[row, "Object"] = str(self.data.loc[row, "Event context"]).split(":")[-1]
        # data = data.drop(columns=['User full name', 'Affected user', 'Description', 'Origin', 'IP address', 'Event context'])
        self.data = self.data[['Time']+['ID']+['Name']+['Component']+['Event name']+['Object']]
    
    def limitbyTime(self, time):
        return self.data.loc[(self.data["Time"] >= time[0]) & (self.data["Time"] <= time[1])]
    
    def findbyAttribute(self, query):
        query = query.split("&")
        res = {}
        for item in query:
            item = item.split("=")
            res[item[0]] = item[1].strip()
        # Query data using pandas
        condition = [True, True, True, True]
        if "id" in res:
            condition[0] = (self.data["ID"]== res["id"])
        if "name" in res:
            condition[1] =  (self.data["Name"]== str(res["name"]))
        if "event" in res:
            condition[2] =  (self.data["Event name"]== str(res["event"]))
        if "component" in res:
            condition[3] =  (self.data["Component"]== str(res["component"]))
        return self.data.loc[condition[0] & condition[1] & condition[2] & condition[3]]
    
    def groupbyComponent(self, attr):
        # Handle query' format
        query = attr.split("&")
        result = self.data.groupby(attr).count()["Time"]
        return result

    def score(self, standard=None):
        lstStudent = self.data.loc[self.data["ID"].notnull()]
        lstID = lstStudent["ID"].unique().tolist()
        result = {}
        for id in lstID:
            result[str(id)] = dict(self.data.loc[self.data["ID"] == id].groupby(["Event name"]).count()["Time"])
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
    
    def listItem(self):
        result = [item.replace(" ", "_") for item in self.data["Event name"].unique().tolist()]
        return result