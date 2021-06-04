import flask, pandas
from flask import request, redirect, url_for, render_template
from functions import functions
import ConnectToMongo

connection = ConnectToMongo.connect("mongodb+srv://bl4ck_29:Matkhau1234@cluster0.otjrb.azure.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# List databases
lstDatabase = connection.list()
lstCollections = []
collection = []
## NOT DONE: Add on more page where users can select database and collection

# Create variables
func = []
query = None
standard = None
# Cleansing data
# func.cleansing()

# Generating API for web
api = flask.Flask(__name__)
api.config["DEBUG"] = True

# NOT DONE: Add homepage
@api.route("/")
def home():
    lstCollections = connection.list(dbName="NCKH")
    return render_template("HomePage.html", collections = lstCollections)

@api.route("/find", methods=["GET"])
def findbyAttribute():
    return func.findbyAttribute(query).to_json(orient="values", default_handler=str)

@api.route("/SetStandard", methods=["GET"])
def SetStandard():
    return render_template("SetStandard.html", items = func.listItem())

@api.route("/dashboard", methods=["GET"])
def score():
    print(type(standard))
    return func.score(standard=standard)


@api.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        if"queryFind" in request.form:
            res = str(request.form["queryFind"])
            global query
            query = res
            return redirect(url_for("findbyAttribute"))

        elif "setStandard" in request.form:
            return redirect(url_for("SetStandard"))
            
        elif "set" in request.form:
            res = dict(request.form)
            for key, value in res.items():
                try:
                    res[key] = int(value)
                except:
                    res[key] = 0
            global standard
            standard = res
            return redirect(url_for("score"))
    
    if request.method == "GET":
        if "colName" in request.args:
            colName = request.args["colName"]
            collection = connection.getData("NCKH", colName, index=False)
            global func
            func = functions.functions(pandas.DataFrame(collection))
            return render_template("test.html")
    else:
        return request.form
api.run()