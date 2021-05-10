# Use for API
from MongoConnection import ConnectToMongo

# Use for console' test
# import ConnectToMongo

import pandas

conn = ConnectToMongo.Connect("mongodb+srv://bl4ck_29:Matkhau1234@cluster0.otjrb.azure.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", "NCKH", "DTH0080-1600817-HK1_2020-2021_20210303-0907")
data = pandas.DataFrame(conn.connect(index=False))
data = data.astype({"Time" : "datetime64"})

def listCollections():
    return (conn.list())

def findbyAttr(query):
    query = query.split("&")
    res = {}
    for item in query:
        item = item.split("=")
        res[item[0]] = item[1].strip()

    ret = [True, True, True, True]
    if "id" in res:
        ret[0] = (data["ID"]== res["id"])
    if "name" in res:
        ret[1] =  (data["Name"]== str(res["name"]))
    if "event" in res:
        ret[2] =  (data["Event name"]== str(res["event"]))
    if "component" in res:
        ret[3] =  (data["Component"]== str(res["component"]))
    return data.loc[ret[0] & ret[1] & ret[2] & ret[3]].to_json(orient="values", default_handler=str)

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

def HomePage(request):
    functions = {
        "List all databases and collections from MongoDB server":"http://127.0.0.1:5000/list",
        "Scores all students according to actions":"http://127.0.0.1:5000/score"
        }
    return functions