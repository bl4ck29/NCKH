def RenderHTMLTable(dctTableBody, lstTableHead):
    if len(dctTableBody) == 0:
        return """<div class='table-scroll table-wrap'><table class='main-table' border='1'></table></div>"""
    tableHeadHTML = "<thead><tr>"
    for label in lstTableHead:
        tableHeadHTML += "<td><h3>%s</h3></td>" % (label)
    tableHeadHTML += "</tr></thead>"

    tableBodyHTML = "<tbody>"
    for key, value in dctTableBody.items():
        tableBodyHTML += "<tr><td class='col-3'>%s</td>"%(key)
        for i in value:
            if i:
                tableBodyHTML += "<td class='col-1'>%s</td>"%(str(i))
            else:
                tableBodyHTML += "<tdclass='col-1'> </tdclass=>"
        tableBodyHTML += "</tr>"
    tableBodyHTML += "</tbody>"
    tableHTML = """<div class='table-scroll table-wrap'><table class='main-table' border='1'>%s</table></div>"""%(tableHeadHTML + tableBodyHTML)

    return tableHTML

def RenderHTMlSelector(name, lstOption):
    option = ""
    for item in lstOption:
        value = str(item).replace(" ", "_")
        option += "<option value='%s'>%s</option>"%(value, item)
    form = """<form action='http://127.0.0.1:5000/submit' method='POST'>
        <label for='object'>Select object: </label>
        <select name='%s'>
        %s
        </select>
        <input type="submit">
        </form>"""%(name, option)
    return form

def CourseInfoHTML(dctCourseInfo):
    infoHTML = """<div>
    <ul>
    <li>CourseID: %s</li>
    <li>Number of student: %d</li>
    <li>Last update: %s</li>
    <li>Lecturer : %s</li>
    </ul></div>
    """%(dctCourseInfo["ID"], dctCourseInfo["numStd"], str(dctCourseInfo["lastUpdate"]), ", ".join(dctCourseInfo["lectures"]))
    return infoHTML