import pandas

def NotDoAssignment(data, typeObject):
    """typeObject must be in list(data[Type]) usually File, Folder, Assignment, Quiz, ...
    """
    # List of studens joined in course and assignment had created
    lstStudents = data.loc[data["ID"].notnull()]["ID"].unique().tolist()
    lstAssignments = data.loc[data["Type"]==typeObject]["Course"].unique().tolist()

    result = {}
    for i in range(len(lstAssignments)):
        # Student had done assignment
        dfStudentsDone = data.loc[(data["Course"]==lstAssignments[i]) & (data["Event"]=="A submission has been submitted.")]
        lstStudentsDone = dfStudentsDone["ID"].unique().tolist()

        for id in lstStudents:
            if id not in result:
                result[id] = []

            if id not in lstStudentsDone:
                result[id].append(None)
            else:
                # Append time of submission
                date = dfStudentsDone.loc[dfStudentsDone["ID"]==id].iloc[0, 0]
                result[id].append(str(date))

        # Count how many student had done assignment and attach to assignment's name
        lstAssignments[i] += "(%d)"%(len(lstStudentsDone))
    return result, lstAssignments

# def RenderHTMLTable(dctStudentDidAssignment, lstAssignments):
#     """dctStudentDidAssignment is a dictionary with students's id as key, list(datetime) as value;
#     lstAssignments is a list of assignments.
#     """
#     # Assignment's name in table head
#     tableHeadHTML = "<thead><tr><td class='fixed-side'></td>"
#     tableHeadHTML += "<td>SUM</td>"
#     for label in lstAssignments:
#         tableHeadHTML += "<td>%s</td>" % (label)
#     tableHeadHTML += "</tr></thead>"

#     tableBodyHTML = "<tbody>"
#     for key, value in dctStudentDidAssignment.items():
#         tableBodyHTML += "<tr><td>%s</td>"%(key)
#         tableBodyHTML += "<td>%d/%d</td>"%((len(value)-value.count(None)), len(value))
#         for i in value:
#             if i:
#                 tableBodyHTML += "<td>%s</td>"%(i)
#             else:
#                 tableBodyHTML += "<td> </td>"
#         tableBodyHTML += "</tr>"
#     tableBodyHTML += "</tbody>"
    
#     tableHTML = "<div class='table-scroll table-wrap'><table class='main-table' border='1'>%s</table></div>"%(tableHeadHTML + tableBodyHTML)

#     return tableHTML

