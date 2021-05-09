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