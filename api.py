import flask
from flask import jsonify, request
from MongoConnection import functions

api = flask.Flask(__name__)
api.config["DEBUG"] = True

@api.route('/find', methods=["GET"])
def find():
    return functions.findbyAttr(request)

@api.route('/stat', methods=["GET"])
def stat():
    return functions.statbyComponent(request)

@api.route('/score', methods=["GET"])
def score():
    return jsonify(functions.score())


api.run()