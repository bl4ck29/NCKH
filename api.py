import flask
from flask import jsonify, request, redirect, url_for, render_template
from functions import functions

api = flask.Flask(__name__)
api.config["DEBUG"] = True
def start():
    api.run()

@api.route('/')
def home():
    return render_template('test.html', collections = functions.listCollections())

@api.route('/find<query>', methods=["GET"])
def find(query):
    return functions.findbyAttr(query)

@api.route('/stat<query>', methods=["GET"])
def stat(query):
    return functions.statbyComponent(query)

@api.route('/score', methods=["GET"])
def score():
    return jsonify(functions.score())

@api.route('/submit', methods=["GET", "POST"])
def submit():
    collection = str(request.args["colName"])
    return collection
api.run()