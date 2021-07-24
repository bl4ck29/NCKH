import flask
from flask import request, redirect, url_for, render_template, jsonify

from datasource import Connection, DataFormater
from function import DataFunctions

connection = Connection.Connection('mongodb+srv://bl4ck_29:Matkhau1234@cluster0.otjrb.azure.mongodb.net/test')

data = None

api = flask.Flask(__name__)
api.config["DEBUG"] = True


@api.route("/listdb", methods=["GET"])
def ListDatabase():
    db = request.args.get('db')
    if db:
        return jsonify(connection.List()[db])
    return jsonify(list(connection.List().keys()))

@api.route("/connect", methods=["POST"])
def Connect():
    db = request.args.get('db')
    col = request.args.get('col')
    if db and col:
        pddata = DataFormater.Convert(connection.LoadData(col=col, db=db))
        global data
        data = DataFunctions.DataFunctions(pddata)
    else:
        data = None
    return request.args

@api.route("/student", methods=["GET"])
def find():
    if request.args == {}:
        return {}
    else:
        return data.FindbyAttribute(request.args).to_json(orient="values", default_handler=str)

@api.route("/items", methods=["GET"])
def ListItems():
    attr = request.args.get("attr")
    return jsonify(data.ListItem(attr))

@api.route("/scores", methods=["GET"])
def Scores():
    standard = request.form
    return jsonify(data.Score(standard= standard))

@api.route("/getTeachersActivities", methods=["GET"])
def GetTeachersActivities():
    return data.GetTeacherActivities()

api.run()