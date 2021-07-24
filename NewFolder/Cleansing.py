import pandas, re
def Cleansing(raw):
    raw = raw.astype({"Time":"datetime64[D]"})
    column = list(raw.columns)
    id_patterns = "[0-9]+[A-Z]+[0-9]+"
    for row in range(len(raw)):
        name = raw.iloc[row, column.index("User full name")]
        lstName = name.split("-")
        match = re.search(id_patterns, name)
        if match:
            raw.loc[row, "ID"] = match.group()

            if len(lstName) < 3:
                startInd = name.index(" ")
                endInd = name.rindex(" ")
                raw.loc[row, "Name"] = str(name[startInd : endInd].strip())

            else:
                raw.loc[row, "Name"] = str(lstName[1].strip())
        else:
            raw.loc[row, "ID"] = pandas.NaT
            raw.loc[row, "Name"] = str(name)
    return raw[['Time']+['ID']+['Name']+['Component']+['Event name']+['Event context']]