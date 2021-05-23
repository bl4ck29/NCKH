import flask, os
from flask import jsonify, request, redirect, url_for, render_template
from pymongo import collection
from pymongo.message import query
from pymongo.mongo_client import MongoClient
from MongoConnection import functions, ConnectToMongo

api = flask.Flask(__name__)
api.config["DEBUG"] = True

@api.route('/')
def home():
    return render_template('test.html', collections=functions.listCollections()["NCKH"])

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
    return collections
api.run()