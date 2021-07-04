import pandas, datetime, re

def Convert(data):
    return pandas.DataFrame(data)

def Cleansing(data):
    data = pandas.DataFrame(data).astype({"Time":"datetime64"})
    columns = list(data.columns)
    pat_id = '[0-9]+[A-Z]+[0-9]+'
    # Handle the empty row in USER FULL NAME
    data.loc[data["User full name"]=="-", "User full name"] = "Admin"
    for row in range(len(data)):
        # Split the time and date from TIME field
        text = str(data.iloc[row, columns.index('Time')]).split(',')
        date = text[0].split("/")
        time = text[1].split(":")
        data.loc[row, "Time"] = datetime.datetime(
            datetime.date.today().year, int(date[1].strip()), int(date[0].strip()), int(time[0].strip()), int(time[1].strip())
            )
        # Search for the student' ID
        name = data.iloc[row, columns.index('User full name')]
        lst = name.split("-")
        match = re.search(pat_id, name)
        if match:
            data.loc[row, "ID"] = match.group()
            # Space instead of - in name
            if len(lst) < 3:
                start = name.index(" ")
                end = name.rindex(" ")
                data.loc[row, "Name"] = str(name[start : end].strip())
            else:
                data.loc[row, "Name"] = str(lst[1].strip())
        else:
            data.loc[row, "ID"] = pandas.NaT
            data.loc[row, "Name"] = str(name)

        if data.loc[row, "Component"] == "Assignment":
            data.loc[row, "Object"] = str(data.loc[row, "Event context"]).split("-")[-1]
        else:
            data.loc[row, "Object"] = str(data.loc[row, "Event context"]).split(":")[-1]
    # data = data.drop(columns=['User full name', 'Affected user', 'Description', 'Origin', 'IP address', 'Event context'])
    return  data[['Time']+['ID']+['Name']+['Component']+['Event name']+['Object']]