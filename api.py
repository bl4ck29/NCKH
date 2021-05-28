from dns.resolver import query
import flask, pandas
from flask import jsonify, request, redirect, url_for, render_template
from functions import functions
import ConnectToMongo

connection = ConnectToMongo.connect("mongodb+srv://bl4ck_29:Matkhau1234@cluster0.otjrb.azure.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# List databases
lstDatabase = connection.list()
lstCollections = []
collection = []
## NOT DONE: Add on more page where users can select database and collection
func = []
# Cleansing data
# func.cleansing()

# Generating API for web
api = flask.Flask(__name__)
api.config["DEBUG"] = True

# NOT DONE: Add homepage
@api.route('/')
def home():    
    # List collections
    lstCollections = connection.list(dbName="NCKH")
    # After select collection, getting data from it
    return render_template('HomePage.html', collections = lstCollections)

@api.route('/find<query>', methods=["GET"])
def find(query):
    return func.findbyAttribute(query).to_json(orient="values", default_handler=str)

@api.route('/stat<query>', methods=["GET"])
def stat(query):
    return func.groupbyComponent(query)

@api.route('/score<lst>', methods=["GET"])
def score(lst):
    if str(type(lst)) == "<class 'dict'>":
        attr = lst["attr"]
        return lst
    else:
        lstItems = func.listItem(lst)
        return render_template("Scores.html", items = lstItems)

# @api.route("/list<attr>", methods=["GET"])
# def list(attr):
#     lstScore = func.listItem(attr)
#     return render_template("Scores.html", items =  lstScore)

@api.route('/submit', methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        if "queryFind" in request.form:
            res = str(request.form["queryFind"])
            return redirect(url_for("find", query = res))

        elif "queryStat" in request.form:
            res = str(request.form["queryStat"])
            return redirect(url_for("stat", query = res))

        elif "queryList" in request.form:
            res = str(request.form["queryList"])
            return redirect(url_for("list", attr = res))

        elif "queryScore" in request.form:
            attr = str(request.form["queryScore"])
            return redirect(url_for("score", lst = attr))

        elif "setStandard" in request.form:
            res = dict(request.form)
            res.pop("setStandard")
            return redirect(url_for("score", lst = res))
    
    if request.method == "GET":
        if "colName" in request.args:
            colName = request.args["colName"]
            collection = connection.getData("NCKH", colName)
            global func
            func = functions.functions(pandas.DataFrame(collection))
            return render_template("test.html")
    else:
        return request.form
    
api.run()