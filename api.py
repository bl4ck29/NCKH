import flask, pymongo, json, pandas
from flask import jsonify, request

connection = pymongo.MongoClient("mongodb+srv://bl4ck_29:Matkhau1234@cluster0.otjrb.azure.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = connection['NCKH']
collection = db['raw_logs']

api = flask.Flask(__name__)
api.config["DEBUG"] = True
query = {}
@api.route('/find', methods=["GET"])
def findby():
    if "id" in request.args:
        query["ID"] = request.args["id"]
    if "name" in request.args:
        query["Name"] = request.args["name"]
    if "event" in request.args:
        query["Event name"] = request.args["event"]
    if "date" in request.args:
        query["Date"] = request.args["date"]
    if "component" in request.args:
        query["Component"] = request.args["component"]
    res = list(collection.find(query, {"_id":0}))
    return jsonify(res)
api.run()