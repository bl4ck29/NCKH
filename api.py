import flask, pandas
from flask import jsonify, request, redirect, url_for, render_template
from functions import functions
import ConnectToMongo

# Load data from MongoDB
connection = ConnectToMongo.connect("mongodb+srv://bl4ck_29:Matkhau1234@cluster0.otjrb.azure.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# List databases and collections
lstDatabase = connection.list()
lstCollections = connection.list(dbName="NCKH")
# After select collection, getting data from it
collection = connection.getData("NCKH", lstCollections[0])


## NOT DONE: Add on more page where users can select database and collection
func = functions.functions(pandas.DataFrame(collection))
# Cleansing data
# func.cleansing()

# Generating API for web
api = flask.Flask(__name__)
api.config["DEBUG"] = True

# NOT DONE: Add homepage
@api.route('/')
def home():
    return render_template('HomePage.html', databases = lstDatabase, collections = [])

@api.route('/find<query>', methods=["GET"])
def find(query):
    return func.findbyAttribute(query).to_json(orient="values", default_handler=str)

@api.route('/stat<query>', methods=["GET"])
def stat(query):
    return func.groupbyComponent(query)

@api.route('/score', methods=["GET"])
def score():
    return jsonify(func.score())

@api.route('/submit', methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        if "queryFind" in request.form:
            res = str(request.form["queryFind"])
            return redirect(url_for("find", query = res))
        elif "queryStat" in request.form:
            res = str(request.form["queryStat"])
            return redirect(url_for("stat", query = res))

    if request.method == "GET":
        dbName = str(request.args["dbName"])
        colName = str(request.args["colName"])
        collection = connection.getData(dbName, colName)
        return render_template("test.html")
    else:
        return "Query cant not be processed"
api.run()