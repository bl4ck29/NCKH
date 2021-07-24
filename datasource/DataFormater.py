import pandas, datetime, re

def Convert(data):
    return pandas.DataFrame(data)

def Cleansing(data):
    data = pandas.DataFrame(data).astype({"Time":"datetime64"})
    columns = list(data.columns)
    pat_id = '[0-9]+[A-Z]+[0-9]+'
    for row in range(len(data)):
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
    return  data[['Time']+['ID']+['Name']+['Component']+['Event name']+['Event context']]