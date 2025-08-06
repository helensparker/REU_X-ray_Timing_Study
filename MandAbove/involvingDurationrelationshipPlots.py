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
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig(f'logdurationinvolved{saveas}.png')
    plt.clf()

def removeMilisecs(difslist):
    newdifslist = []
    removeindlist = []
    for i in range(len(difslist)):
        newdifslist.append(difslist[i][2:7])
    return [newdifslist,removeindlist]

def removemilisecsdur(durlist):
    newdurlist = []
    for i in range(len(durlist)):
        newdurlist.append(durlist[i][0:7])
    return newdurlist

def convertToSeconds(timelist):
    sList = []
    for t in timelist:
        sep = list(map(int, t.split(":")))
        if len(sep) == 3:
            h, m, s = sep
        elif len(sep) == 2:
            h = 0
            m, s = sep
        realsecs = h*3600 + m*60+s
        sList.append(realsecs)
    return sList

def divduration(difs,dur):
    divdurlist = []
    for i in range(len(difs)):
        divdurlist.append(difs[i]/dur[i])
    return divdurlist


df = pd.read_csv('newtimeDifsPeaktimesandVals.csv')

difs18 = df['1.0-8.0A_time_until_peak'].tolist()
difs54 = df['0.5-4.0A_time_until_peak'].tolist()

difs410 = df['4-10keV_time_until_peak'].tolist()
difs1015 = df['10-15keV_time_until_peak'].tolist()
difs1525 = df['15-25keV_time_until_peak'].tolist()
difs2550 = df['25-50keV_time_until_peak'].tolist()
difs5084 = df['50-84keV_time_until_peak'].tolist()

duration = df['duration'].tolist()

alldifs18 = removeMilisecs(difs18)
alldifs54 = removeMilisecs(difs54)
alldifs410 = removeMilisecs(difs410)
alldifs1015 = removeMilisecs(difs1015)
alldifs1525 = removeMilisecs(difs1525)
alldifs2550 = removeMilisecs(difs2550)
alldifs5084 = removeMilisecs(difs5084)

duration = removemilisecsdur(duration)

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

duration = convertToSeconds(duration)

difs18 = divduration(difs18,duration)
difs54 = divduration(difs54,duration)
difs410 = divduration(difs410,duration)
difs1015 = divduration(difs1015,duration)
difs1525 = divduration(difs1525,duration)
difs2550 = divduration(difs2550,duration)
difs5084 = divduration(difs5084,duration)


consTitle = 'Hard & Soft X-rays Peak Time Since Start of Flare'

scatterPlot(difs18,difs410,consTitle,'SXR Time from Start of Flare (1.0-8.0A)/duration','HXR Time from Start of Flare (4-10keV)/duration','difs18difs410')
scatterPlot(difs18,difs1015,consTitle,'SXR Time from Start of Flare (1.0-8.0A)/duration','HXR Time from Start of Flare (10-15keV)/duration','difs18difs1015')
scatterPlot(difs18,difs1525,consTitle,'SXR Time from Start of Flare (1.0-8.0A)/duration','HXR Time from Start of Flare (15-25keV)/duration','difs18difs1525')
scatterPlot(difs18,difs2550,consTitle,'SXR Time from Start of Flare (1.0-8.0A)/duration','HXR Time from Start of Flare (25-50keV)/duration','difs18difs2550')
scatterPlot(difs18,difs5084,consTitle,'SXR Time from Start of Flare (1.0-8.0A)/duration','HXR Time from Start of Flare (50-84keV)/duration','difs18difs5084')

scatterPlot(difs54,difs410,consTitle,'SXR Time from Start of Flare (0.5-4.0A)/duration','HXR Time from Start of Flare (4-10keV)/duration','difs54difs410')
scatterPlot(difs54,difs1015,consTitle,'SXR Time from Start of Flare (0.5-4.0A)/duration','HXR Time from Start of Flare (10-15keV)/duration','difs54difs1015')
scatterPlot(difs54,difs1525,consTitle,'SXR Time from Start of Flare (0.5-4.0A)/duration','HXR Time from Start of Flare (15-25keV)/duration','difs54difs1525')
scatterPlot(difs54,difs2550,consTitle,'SXR Time from Start of Flare (0.5-4.0A)/duration','HXR Time from Start of Flare (25-50keV)/duration','difs54difs2550')
scatterPlot(difs54,difs5084,consTitle,'SXR Time from Start of Flare (0.5-4.0A)/duration','HXR Time from Start of Flare (50-84keV)/duration','difs54difs5084')
