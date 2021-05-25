import pandas, re, datetime

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
            # data.loc[row, 'Date'] = datetime.date(datetime.date.today().year, int(date[1].strip()), int(date[0].strip()))
            time = text[1].split(":")
            # data.loc[row, 'Time'] = datetime.time(int(time[0].strip()), int(time[1].strip()))
            self.data.loc[row, "Time"] = datetime.datetime(datetime.date.today().year, int(date[1].strip()), int(date[0].strip()), int(time[0].strip()), int(time[1].strip()))
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
    
    def groupbyComponent(self, query):
        # Default
        lstEnrolled = ["There is nothing to return here"]
        # Handle query' format
        query = query.split("&")
        result = self.data.groupby(query).count()["Time"]
        # if "component" in query:
        #     lstEnrolled = self.data.groupby(["Component"]).count()
        #     # lstEnrolled = pandas.DataFrame(self.data.loc[self.data["Component"] == query]["ID"].unique())
        # if "event" in query:
        #     lstEnrolled = self.data.groupby(["Event name"]).count()
        #     # lstEnrolled = pandas.DataFrame(self.data.loc[self.data["Event name"] == query]["ID"].unique(), columns=[["ID"]])
        # if "object" in query:
        #     lstEnrolled = self.data.groupby(["Object"]).count()
        #     # lstEnrolled = pandas.DataFrame(self.data.loc[self.data["Object"] == query]["ID"].unique(), columns=["ID"])
        return result.to_dict()

    def score(self):
        dct = {}
        sample = pandas.DataFrame(self.data.groupby(["ID", "Component", "Event name"]).count())
        for row in range(len(sample)):
            id = str(self.data.loc[row, "ID"])
            comp = str(self.data.loc[row, "Component"])
            event = str(self.data.loc[row, "Event name"])
            if id in dct:
                if comp in dct[id]:
                    if event not in dct[id][comp]:
                        dct[id][comp].append(event)
                else:
                    dct[id][comp] = [event]
            else:
                dct[id] = {comp : [event]}

        standard = self.data["Event name"].unique().tolist()
        if "nan" in dct:
            dct.pop("nan")
        for key, value in dct.items():
            score = 0
            for k, v in value.items():
                for i in v:
                    if i in standard:
                        score += 1
            dct[key] = score
        return dct