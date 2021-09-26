import flask
import pandas
import subprocess
import os
from flask import request, redirect, url_for, render_template, jsonify
from function import OverviewTable, DataFrameFunction, ScorebyEventName, ConfigParser, RenderToHTML
from function.ChartData import ChartData

apiMain = flask.Flask(__name__)
apiMain.config["DEBUG"] = True
apiMain.config["CACHE_TYPE"] = "null"
apiMain.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


data = None
PATH_LogFile = None

@apiMain.route("/", methods=["GET"])
def Home():
    global PATH_LogFile
    PATH_LogFile = ConfigParser.Get("PATH", "LogFile")
    os.chdir(PATH_LogFile)
    LISTFILENAME = list(filter(lambda x: ".csv" in x, list(os.listdir())))
    # return render_template("HomePage.html", content="", lstCourseID=LISTFILENAME)
    return render_template("StartPage.html", lstObj = LISTFILENAME)


@apiMain.route("/homepage", methods=["GET"])
def Introduce():
    global data
    form = None
    PATH_HomePageText = ConfigParser.Get("PATH", "Introduction")
    PATH_HomePageText += request.args.get("obj").capitalize() + ".txt"
    if request.args.get("obj") =="overview":
        form = OverviewTable.RenderHTMlSelector("course-object", DataFrameFunction.ListObjectName(data))
    if request.args.get("obj") == "visualization":
        form = OverviewTable.RenderHTMlSelector("typename", ["Assignment", "Quiz", "File", "Folder"])
    content = open(PATH_HomePageText, encoding="utf-8").read().split("---")
    return render_template('Intro.html', introHeader=content[0], introContent=content[1], form = form)


@apiMain.route("/activities/overview", methods=["GET"])
def Overview(obj):
    global data
    dctStudentDidAssignment, lstAssignments = OverviewTable.NotDoAssignment(data, obj)
    lstAssignments.insert(0, "SUM")
    for key, value in dctStudentDidAssignment.items():
        pct = round((1-(value.count(None)/len(value)))*100, -1)
        dctStudentDidAssignment[key].insert(0, str(pct)+"%")
    tableHTML = OverviewTable.RenderHTMLTable(dctStudentDidAssignment, lstAssignments)
    return render_template("base.html", content=tableHTML)


@apiMain.route("/setstandard", methods=["GET"])
def SetStandard():
    return render_template("SetStandard.html", items=DataFrameFunction.listItem(data, "Event"), content="")


# @apiMain.route("/score", methods=["GET"])
# def Dashboard(standard):
#     global data
#     dctAssignment, lstAssignment = OverviewTable.NotDoAssignment(data, "Assignment")
#     dctQuiz, lstQuiz = OverviewTable.NotDoAssignment(data, "Assignment")
#     dctFile, lstFile = OverviewTable.NotDoAssignment(data, "File")

#     for key, value in standard.items():
#         try:
#             standard[key] = int(value)
#         except:
#             standard[key] = 1
#     result = ScorebyEventName.Score(data, standard=standard)

#     for key in result:
#         pctAssignment = round(
#             (1-(dctAssignment[key].count(None)/len(dctAssignment[key])))*100, -1)
#         pctQuiz = round(
#             (1-(dctQuiz[key].count(None)/len(dctQuiz[key])))*100, -1)
#         pctFile = round(
#             (1-(dctFile[key].count(None)/len(dctFile[key])))*100, -1)
#         result[key] = [result[key], pctAssignment, pctQuiz, pctFile]
#     return render_template("base.html",
#                            content=OverviewTable.RenderHTMLTable(result, ["Score", str(len(lstAssignment))+" Assignments(%)", str(len(lstQuiz))+" Quizzes(%)", str(len(lstFile))+" Files(%)"]))

@apiMain.route("/dashboard", methods=['GET'])
def Dashboard(filename, lstObject):
    global data
    os.system('rm /home/vlu-fit/NCKH/static/*.jpeg')
    chartGener = ChartData(data.loc[data["ID"].notnull()])

    infoHTML = ""
    chartHTML = ""
    for typename in ["File", "Assignment" ,"Quiz"]:
        lstDone, lstNotDone, lst = chartGener.StackBarChartData(typename)
        imgName = chartGener.StackBarChart(typename)
        print(imgName)
        dct = {}
        for i in range(len(lst)):
            dct[lst[i]] = [round((lstDone[i]/ (lstDone[i] + lstNotDone[i]))*100, 2)]
        infoHTML +=  "<td>%s</td>" %RenderToHTML.RenderHTMLTable(dct, [typename, "%"])
        chartHTML += "<td><img src='%s' alt='%s'></td>"%("./static/"+ imgName, imgName)

    lstStudent = data["ID"].unique().tolist()
    dctCourseInfo = {"ID":filename.replace(".csv", ""), "numStd":len(lstStudent)}

    return render_template("Dashboard.html", imgname=chartGener.ComponentPieChart() ,course_info = RenderToHTML.CourseInfoHTML(dctCourseInfo), info=infoHTML, chart=chartHTML, lstObj=lstObject)

@apiMain.route("/submit", methods=["GET", "POST"])
def submit():
    global data
    if request.method == "POST":
        if "typename" in request.form:
            return Overview(request.form["typename"])
        elif "filename" in request.form:
            FILENAME = request.form["filename"]
            data = pandas.read_csv(PATH_LogFile + FILENAME).astype({"Time": "datetime64"})
            return Dashboard(FILENAME, data["ID"].unique().tolist())
        elif "setstandard" in request.form:
            return Dashboard(dict(request.form))
        elif "course-object" in request.form:
            return DataFrameFunction.FindByAttribute(data, {"Course": str(request.form["course-object"]).replace("_", " ")}).to_html()
        elif "student" in request.form:
            id = request.form["student"]
            data = data.loc[data["ID"]==id]
            return Dashboard(id, [id])
        else:
            return request.form

    elif request.method == "GET":
        if "test" in request.args:
            return render_template("index.html", content=open("../templates/test.html").read())
    else:
        return request.args

apiMain.run()