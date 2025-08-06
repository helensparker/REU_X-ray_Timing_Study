import pandas as pd
import csv

def mAndXforThreshold(flarelist,thresholdlist):
    all,x,m = 0,0,0
    for i in range(len(thresholdlist)):
        if thresholdlist[i] != 'nan':
            all += 1
            if flarelist[i][0] == 'X':
                x += 1
            elif flarelist[i][0] == 'M':
                m += 1
    return m/all, x/all

df = pd.read_csv('integral.csv')

th1 = df['1.18*10^4_time'].astype(str).tolist()
th2 = df['8.27*10^5_time'].astype(str).tolist()
th3 = df['1.22*10^6_time'].astype(str).tolist()
classes = df['flare_class'].astype(str).tolist()

mperc1, xperc1 = mAndXforThreshold(classes,th1)
mperc2, xperc2 = mAndXforThreshold(classes,th2)
mperc3, xperc3 = mAndXforThreshold(classes,th3)

list1 = [1.18*10**4,mperc1,xperc1]
list2 = [8.27*10**5,mperc2,xperc2]
list3 = [1.22*10**6,mperc3,xperc3]

with open('thresholdTable.csv', 'a', newline='') as file :
    writer = csv.writer(file)
    writer.writerow(list1)
    writer.writerow(list2)
    writer.writerow(list3)