import pandas

def Score(data, standard=None):
    # Get students list
    lstStudent = data.loc[data["ID"].notnull()]
    lstID = lstStudent["ID"].unique().tolist()

    result = {}
    #  Count times doing event {"ID": {"Event" : times}}
    for id in lstID:
        result[str(id)] = dict(data.loc[data["ID"] == id].groupby(["Event"]).count()["Time"])

    for id, value in result.items():
        sumScore = 0
        for item, time in value.items():
            try:
                time = int(time)
                item = item.replace(" ", "_")
                if item in standard:
                    score = standard[item]
                else:
                    score = 1
                sumScore += time * score
            except:
                sumScore += 0
        result[id] = sumScore
    return result