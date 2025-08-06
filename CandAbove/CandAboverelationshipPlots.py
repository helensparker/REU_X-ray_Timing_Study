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
    #plt.xscale('log')
    #plt.yscale('log')
    plt.savefig(f'CandAbove{saveas}.png')
    plt.clf()

def removeMilisecs(difslist):
    newdifslist = []
    removeindlist = []
    for i in range(len(difslist)):
        newdifslist.append(difslist[i][2:7])
    return [newdifslist,removeindlist]

def convertToSeconds(timelist):
    sList = []
    for t in timelist:
        m, s = map(int, t.split(":"))
        realsecs = m * 60 + s
        sList.append(realsecs)
    return sList

df = pd.read_csv('CandAbovetimeDifsPeaktimesandVals.csv')

difs18 = df['1.0-8.0A_time_until_peak'].tolist()

difs410 = df['4-10keV_time_until_peak'].tolist()
difs1015 = df['10-15keV_time_until_peak'].tolist()
difs1525 = df['15-25keV_time_until_peak'].tolist()
difs2550 = df['25-50keV_time_until_peak'].tolist()
difs5084 = df['50-84keV_time_until_peak'].tolist()

alldifs18 = removeMilisecs(difs18)
alldifs410 = removeMilisecs(difs410)
alldifs1015 = removeMilisecs(difs1015)
alldifs1525 = removeMilisecs(difs1525)
alldifs2550 = removeMilisecs(difs2550)
alldifs5084 = removeMilisecs(difs5084)

difs18 = alldifs18[0]
difs410 = alldifs410[0]
difs1015 = alldifs1015[0]
difs1525 = alldifs1525[0]
difs2550 = alldifs2550[0]
difs5084 = alldifs5084[0]

difs18 = convertToSeconds(difs18)
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
