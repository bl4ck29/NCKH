import pandas, datetime, os, numpy, datetime
import matplotlib.pyplot as plt
from function import DataFrameFunction, ConfigParser

class ChartData:
    def __init__(self, dfData, stdID=None):
        if stdID:
            self.dfData = dfData.loc[dfData["ID"]==stdID].astype({"Time":"datetime64"})
        else:
            self.dfData = dfData.astype({"Time":"datetime64"})
        self.PATH = ConfigParser.Get("PATH", "ChartImage")
    
    def ComponentPieChart(self):
        """Draw pie chart show the percentage of component counted by numbers of activities
        (return): File path to chart's image
        """
        dct = dict(self.dfData.groupby(["Component"]).count()["ID"])
        lstKeys = list(dct.keys())
        lstValues = list(dct.values())

        s = 0
        other = []
        while len(lstValues) > 5:
            indMinValue = lstValues.index((min(lstValues)))
            s += lstValues.pop(indMinValue)
            
            key = lstKeys.pop(indMinValue)
            other.append(key)
            dct.pop(key)
        dct["Other"] = s

        sizes = list(dct.values())
        labels = list(dct.keys())
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        FILENAME = "ComponentPieChart_%s.jpeg"%str(datetime.datetime.now())
        plt.savefig(self.PATH + FILENAME)
        return FILENAME
    
    def ProcessLineChart(self, stdID):
        """
        """
        sample = self.dfData.loc[self.dfData["ID"]==stdID]
        startDate = self.dfData.iloc[len(sample), 0]
        endDate = self.dfData.iloc[0, 0]
        periods = (endDate - startDate).days // 10
        dctResult = {}
        while startDate <= endDate:
            time = startDate + datetime.timedelta(days=periods)
            limitByTime = DataFrameFunction.LimitByTime(sample, startDate, time)
            dctResult[time] = len(limitByTime)
            startDate = time
        print(dctResult)
        plt.plot(list(dctResult.keys()), list(dctResult.values()))
        plt.xticks(rotation=90)
        plt.title("Event chart")
        FILENAME = "ProcessLineChart_%s.jpeg"%str(datetime.datetime.now())
        plt.savefig(self.PATH + FILENAME)
        return FILENAME

    def StackBarChartData(self, typename):
        sample = self.dfData.loc[self.dfData["ID"].notnull()]
        numStudent = len(sample["ID"].unique().tolist())
        lstType = sample.loc[sample["Type"]==typename]["Course"].unique().tolist()
        lstDone = []
        lstNotDone = []
        for file in lstType:
            done = len(sample.loc[(sample["Type"]==typename) & (sample["Course"]==file)]["ID"].unique().tolist())
            lstDone.append(done)
            lstNotDone.append(numStudent-done)
        return lstDone, lstNotDone, lstType
    
    def StackBarChart(self, typename):
        done , notdone, lst = self.StackBarChartData(typename)
        fig, ax = plt.subplots(figsize=(18, 10))
        p1 = ax.bar(lst, done, 0.35, label="Done")
        p2 = ax.bar(lst, notdone, 0.35,bottom=done, label="NotDone")

        ax.set_ylabel("Number of students")
        ax.set_xticks(numpy.arange(len(lst)))
        ax.set_xticklabels(lst)
        ax.legend()
        ax.bar_label(p1, label_type="center")
        ax.bar_label(p2, label_type="center")

        plt.xticks(rotation=45)
        FILENAME = typename + "StackBarChar_%s.jpeg"%str(datetime.datetime.now())
        plt.savefig(self.PATH + FILENAME)
        return FILENAME