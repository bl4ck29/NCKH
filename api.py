import flask
from flask import jsonify, request, redirect, url_for
from MongoConnection import functions, ConnectToMongo

api = flask.Flask(__name__)
api.config["DEBUG"] = True

@api.route('/', methods=["GET"])
def home():
    lstFunctions = functions.HomePage(request)
    res = ""
    for function, link in lstFunctions.items():
        res += '<a href="%s" target="_blank">%s</a></br>'%(link, function)
    return res

@api.route('/find<query>', methods=["GET"])
def find(query):
    return functions.findbyAttr(query)

@api.route('/stat', methods=["GET"])
def stat():
    return functions.statbyComponent(request)

@api.route('/score', methods=["GET"])
def score():
    return jsonify(functions.score())

@api.route('/list', methods=["GET"])
def list():
    return jsonify(functions.listCollections())

@api.route('/submit/attr', methods=["POST"])
def submit():
    res = str(request.form["txtQuery"])
    return redirect(url_for("find", query = res))

api.run()