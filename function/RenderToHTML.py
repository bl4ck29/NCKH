def RenderHTMLTable(dctTableBody, lstTableHead):
    tableHeadHTML = "<thead><tr>"
    for label in lstTableHead:
        tableHeadHTML += "<td><h3>%s</h3></td>" % (label)
    tableHeadHTML += "</tr></thead>"

    tableBodyHTML = "<tbody>"
    for key, value in dctTableBody.items():
        tableBodyHTML += "<tr><td>%s</td>"%(key)
        for i in value:
            if i:
                tableBodyHTML += "<td>%s</td>"%(str(i))
            else:
                tableBodyHTML += "<td> </td>"
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
    <li>Last update: </li>
    <li>Lecturer : </li>
    </ul></div>
    """%(dctCourseInfo["ID"], dctCourseInfo["numStd"])
    return infoHTML