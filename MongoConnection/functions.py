# Use for API
from MongoConnection import ConnectToMongo

# Use for console' test
# import ConnectToMongo

import pandas

data = pandas.DataFrame(ConnectToMongo.connect("mongodb+srv://bl4ck_29:Matkhau1234@cluster0.otjrb.azure.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"))
data = data.astype({"Time" : "datetime64"})

def findbyAttr(request):
    query = [True, True, True, True]
    if "id" in request.args:
        query[0] = (data["ID"]== str(request.args["id"]).upper())
    if "name" in request.args:
        query[1] =  (data["Name"]== str(request.args["name"]))
    if "event" in request.args:
        query[2] =  (data["Event name"]== str(request.args["event"]))
    if "component" in request.args:
        query[3] =  (data["Component"]== str(request.args["component"]))
    return data.loc[query[0] & query[1] & query[2] & query[3]].to_json(orient="values")

def statbyComponent(request):
    if "component" in request.args:
        lstEnrolled = pandas.DataFrame(data.loc[data["Component"] == request.args["component"]]["ID"].unique(), columns=["ID"])
    if "event" in request.args:
        lstEnrolled = pandas.DataFrame(data.loc[data["Event name"] == request.args["event"]]["ID"].unique(), columns=[request.args["ID"]])
    if "object" in request.args:
        lstEnrolled = pandas.DataFrame(data.loc[data["Object"] == request.args["object"]]["ID"].unique(), columns=["ID"])
    return lstEnrolled.to_json(orient="values")

def limitbyTime(time):
    return data.loc[(data["Time"] >= time[0]) & (data["Time"] <= time[0])]

def score():
    dct = {}
    sample = pandas.DataFrame(data.groupby(["ID", "Component", "Event name"]).count())
    for row in range(len(sample)):
        id = str(data.loc[row, "ID"])
        if id in dct:

            comp = str(data.loc[row, "Component"])
            if comp in dct[id]:

                event = str(data.loc[row, "Event name"])
                if event not in dct[id][comp]:
                    dct[id][comp].append(event)

            else:
                dct[id][comp] = []
        else:
            dct[id] = {}

    standard = data["Event name"].unique().tolist()
    dct.pop("")
    for key, value in dct.items():
        score = 0
        for k, v in value.items():
            for i in v:
                if i in standard:
                    score += 1
        dct[key] = score
    return dct