import pandas, re, os, datetime
# Navigation to the log file folder
curDir = os.getcwd()
sourceDir = curDir[:curDir.rindex("\\")] + "\\Log files"
desDir = curDir[:curDir.rindex("\\")] + "\\result\\"
os.mkdir(desDir)

os.chdir(sourceDir)
# Get the list of log files
listFile = list(filter(lambda name: ".csv" in name, os.listdir()))

for file in listFile:
    data = pandas.read_csv(sourceDir + "\\" +file)

    cols = list(data.columns)
    pat_id = '[0-9]+[A-Z]+[0-9]+'

    # Handle the empty row in USER FULL NAME
    data.loc[data["User full name"]=="-", "User full name"] = "Admin"
    
    for row in range(len(data)):
        # Split the time and date from TIME field
        text = str(data.iloc[row, cols.index('Time')]).split(',')
        date = text[0].split("/")
        # data.loc[row, 'Date'] = datetime.date(datetime.date.today().year, int(date[1].strip()), int(date[0].strip()))
        time = text[1].split(":")
        # data.loc[row, 'Time'] = datetime.time(int(time[0].strip()), int(time[1].strip()))
        data.loc[row, "Time"] = datetime.datetime(datetime.date.today().year, int(date[1].strip()), int(date[0].strip()), int(time[0].strip()), int(time[1].strip()))
        
        # Search for the student' ID
        name = data.iloc[row, cols.index('User full name')]
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

    data = data.drop(columns=['User full name', 'Affected user', 'Description', 'Origin', 'IP address', 'Event context'])

    data = data[['Time']+['ID']+['Name']+['Component']+['Event name']+['Object']]
    data.to_csv(desDir + "\\" + file, index=False)