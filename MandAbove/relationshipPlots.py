import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime
from datetime import time
from datetime import timedelta
import csv
import matplotlib.ticker as ticker

def scatterPlot(sxrlist,hxrlist,title,xlab,ylab,saveas):
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    plt.scatter(sxrlist,hxrlist)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    #plt.show()
    plt.savefig(f'{saveas}.png')
    plt.clf()

def removeMilisecs(difslist):
    newdifslist = []
    removeindlist = []
    for i in range(len(difslist)):
        if difslist[i][2:7] == ' day,':
            removeindlist.append(i)
            newdifslist.append('0:00')
        else:
            newdifslist.append(difslist[i][2:7])
    return [newdifslist,removeindlist]

def combineindlist(list1,list2,list3,list4,list5,list6,list7):
    fullindlist = list1
    for i in list2:
        if not i in fullindlist:
            fullindlist.append(i)
    for i in list3:
        if not i in fullindlist:
            fullindlist.append(i)
    for i in list4:
        if not i in fullindlist:
            fullindlist.append(i)
    for i in list5:
        if not i in fullindlist:
            fullindlist.append(i)
    for i in list6:
        if not i in fullindlist:
            fullindlist.append(i)
    for i in list7:
        if not i in fullindlist:
            fullindlist.append(i)
    fullindlist.sort(reverse = True)
    print(fullindlist)
    return fullindlist

def removal(list1,list2,list3,list4,list5,list6,list7):
    indicesToRemove = combineindlist(list1[1],list2[1],list3[1],list4[1],list5[1],list6[1],list7[1])
    indicesToRemove = sorted(set(indicesToRemove), reverse=True)
    for i in indicesToRemove:
        del list1[0][i]
        del list2[0][i]
        del list3[0][i]
        del list4[0][i]
        del list5[0][i]
        del list6[0][i]
        del list7[0][i]
    return [list1[0],list2[0],list3[0],list4[0],list5[0],list6[0],list7[0]]



#Change this even if it works to something I fully get
def convertToSeconds(timestrlist):
    seconds_list = []
    for t in timestrlist:
        minutes, seconds = map(int, t.split(":"))
        total_seconds = minutes * 60 + seconds
        seconds_list.append(total_seconds)
    return seconds_list

df = pd.read_csv('timeDifsPeaktimesandVals.csv')

difs18 = df['1.0-8.0A_time_until_peak'].tolist()
difs54 = df['0.5-4.0A_time_until_peak'].tolist()

difs410 = df['4-10keV_time_until_peak'].tolist()
difs1015 = df['10-15keV_time_until_peak'].tolist()
difs1525 = df['15-25keV_time_until_peak'].tolist()
difs2550 = df['25-50keV_time_until_peak'].tolist()
difs5084 = df['50-84keV_time_until_peak'].tolist()

alldifs18 = removeMilisecs(difs18)
alldifs54 = removeMilisecs(difs54)
alldifs410 = removeMilisecs(difs410)
alldifs1015 = removeMilisecs(difs1015)
alldifs1525 = removeMilisecs(difs1525)
alldifs2550 = removeMilisecs(difs2550)
alldifs5084 = removeMilisecs(difs5084)

difs18 = alldifs18[0]
difs54 = alldifs54[0]
difs410 = alldifs410[0]
difs1015 = alldifs1015[0]
difs1525 = alldifs1525[0]
difs2550 = alldifs2550[0]
difs5084 = alldifs5084[0]

difs18 = convertToSeconds(difs18)
difs54 = convertToSeconds(difs54)
difs410 = convertToSeconds(difs410)
difs1015 = convertToSeconds(difs1015)
difs1525 = convertToSeconds(difs1525)
difs2550 = convertToSeconds(difs2550)
difs5084 = convertToSeconds(difs5084)


consTitle = 'Hard & Soft X-rays Peak Time Since Start of Flare'

scatterPlot(difs18,difs410,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (4-10keV) (s)','difs18difs410')
scatterPlot(difs18,difs1015,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (10-15keV) (s)','difs18difs1015')
scatterPlot(difs18,difs1525,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (15-25keV) (s)','difs18difs1525')
scatterPlot(difs18,difs2550,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (25-50keV) (s)','difs18difs2550')
scatterPlot(difs18,difs5084,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (50-84keV) (s)','difs18difs5084')

scatterPlot(difs54,difs410,consTitle,'SXR Time from Start of Flare (0.5-4.0A) (s)','HXR Time from Start of Flare (4-10keV) (s)','difs54difs410')
scatterPlot(difs54,difs1015,consTitle,'SXR Time from Start of Flare (0.5-4.0A) (s)','HXR Time from Start of Flare (10-15keV) (s)','difs54difs1015')
scatterPlot(difs54,difs1525,consTitle,'SXR Time from Start of Flare (0.5-4.0A) (s)','HXR Time from Start of Flare (15-25keV) (s)','difs54difs1525')
scatterPlot(difs54,difs2550,consTitle,'SXR Time from Start of Flare (0.5-4.0A) (s)','HXR Time from Start of Flare (25-50keV) (s)','difs54difs2550')
scatterPlot(difs54,difs5084,consTitle,'SXR Time from Start of Flare (0.5-4.0A) (s)','HXR Time from Start of Flare (50-84keV) (s)','difs54difs5084')

exit()


alldifs18 = [difs18,alldifs18[1]]
alldifs54 = [difs54,alldifs54[1]]
alldifs410 = [difs410,alldifs410[1]]
alldifs1015 = [difs1015,alldifs1015[1]]
alldifs1525 = [difs1525,alldifs1525[1]]
alldifs2550 = [difs2550,alldifs2550[1]]
alldifs5084 = [difs5084,alldifs2550[1]]

print(len(difs5084))
print(difs5084)
newlists = removal(alldifs18,alldifs54,alldifs410,alldifs1015,alldifs1525,alldifs2550,alldifs5084)

difs18 = newlists[0]
difs54 = newlists[1]
difs410 = newlists[2]
difs1015 = newlists[3]
difs1525 = newlists[4]
difs2550 = newlists[5]
difs5084 = newlists[6]

#print(len(difs5084))
#print(difs5084)
exit()

consTitle = 'Hard & Soft X-rays Peak Time Since Start of Flare'

scatterPlot(difs18,difs410,consTitle,'SXR Time from Start of Flare (1.0-8.0A)','HXR Time from Start of Flare (4-10keV)','difs18difs410')
scatterPlot(difs18,difs1015,consTitle,'SXR Time from Start of Flare (1.0-8.0A)','HXR Time from Start of Flare (10-15keV)','difs18difs1015')
scatterPlot(difs18,difs1525,consTitle,'SXR Time from Start of Flare (1.0-8.0A)','HXR Time from Start of Flare (15-25keV)','difs18difs1525')
scatterPlot(difs18,difs2550,consTitle,'SXR Time from Start of Flare (1.0-8.0A)','HXR Time from Start of Flare (25-50keV)','difs18difs2550')
scatterPlot(difs18,difs5084,consTitle,'SXR Time from Start of Flare (1.0-8.0A)','HXR Time from Start of Flare (50-84keV)','difs18difs5084')

scatterPlot(difs54,difs410,consTitle,'SXR Time from Start of Flare (0.5-4.0A)','HXR Time from Start of Flare (4-10keV)','difs54difs410')
scatterPlot(difs54,difs1015,consTitle,'SXR Time from Start of Flare (0.5-4.0A)','HXR Time from Start of Flare (10-15keV)','difs54difs1015')
scatterPlot(difs54,difs1525,consTitle,'SXR Time from Start of Flare (0.5-4.0A)','HXR Time from Start of Flare (15-25keV)','difs54difs1525')
scatterPlot(difs54,difs2550,consTitle,'SXR Time from Start of Flare (0.5-4.0A)','HXR Time from Start of Flare (25-50keV)','difs54difs2550')
scatterPlot(difs54,difs5084,consTitle,'SXR Time from Start of Flare (0.5-4.0A)','HXR Time from Start of Flare (50-84keV)','difs54difs5084')
