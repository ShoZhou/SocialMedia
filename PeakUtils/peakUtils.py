import csv
import numpy as np
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot

file = "C:/Users/57194/Desktop/社交媒体/PeakUtils/乐队的夏天2.csv"
dates = []
# dic_res = dict.fromkeys(dates,0)

#构建日期为key的字典，dates存放所有日期
with open(file, 'r', encoding='UTF-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date = row["date"]
        if (date not in dates):
            dates.append(row["date"])
# print(dates)
#构建日期为key的字典来保存计数，dic_res存放结果
dic_res = dict.fromkeys(dates, 0)


with open(file, 'r', encoding='UTF-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date = row["date"]
        if (date not in dates):
            dates.append(row["date"])
        dic_res[date] = dic_res[date] + 1
# print(dic_res)

x = []
y = []
for key in dic_res:
    x.append(key)
    # print(key)
    y.append(dic_res[key])
    # print(dic_res[key])

#取2020-01-01 到 2020-10-21的数据
x = x[200:443]
y = y[200:443]
x = np.array(x)
y = np.array(y)
indexes = peakutils.indexes(np.array(y), thres=0.1, min_dist=2)
# print(indexes)
print(x[indexes], y[indexes])
pyplot.figure(figsize=(500, 7))
pplot(x, y, indexes)
# print(x)
ax = pyplot.gca()
ax.set_xticks([1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111,
               121, 131, 141, 151, 161, 171, 181, 191, 201, 211, 221, 231, 241])
# ax.set_xticks([1:242:10])
ax.set_xticklabels(x[1:242:10])
# print(x[1:142:10])
pyplot.xticks(size='small', rotation=68, fontsize=9)
for index in indexes:
    pyplot.bar(x[index], y[index], 0.3, color="slateblue")
    pyplot.text(x[index], y[index], x[index], fontsize=10,
                ha='center', va='bottom', color="slateblue", weight="bold")
pyplot.title("PeakUtil from 2020-01-01 to 2020-10-21")
pyplot.show()

for date in indexes:
    print(x[date])