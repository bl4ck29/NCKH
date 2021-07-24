from Cleansing import Cleansing
import Functions
import pandas, datetime
import matplotlib.pyplot as plt

data = Cleansing(pandas.read_csv("D:/NCKH/Log files/DIT0090-05B0185-HK1_2020-2021_20210304-1826.csv", nrows=2000))
lstCol = list(data.columns)

name = "A submission has been submitted."
context = "Assignment: Nộp báo cáo cá nhân_nhóm thực hành IT02-02 (ca4:15g30) học chiều thứ 6"
sample = data.loc[(data["ID"].notnull())]

startTime = sample.sort_values(["Time"], ascending=True).iloc[0, lstCol.index("Time")]
endTime = sample.sort_values(["Time"], ascending=True).iloc[-1, lstCol.index("Time")]
weeks = (endTime - startTime).days //7

lstX = []
lstY = []
while startTime < endTime:
    time = startTime + datetime.timedelta(days=7)
    if len(lstX) == 0:
        lstX.append(7)
    else:
        lstX.append(lstX[-1] +7)
    lstY.append(len(sample.loc[(sample["Time"]>=startTime) & (sample["Time"]<time)]))
    startTime = time
print(lstY)
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(lstX, lstY)
plt.xticks(rotation=60)
plt.show()