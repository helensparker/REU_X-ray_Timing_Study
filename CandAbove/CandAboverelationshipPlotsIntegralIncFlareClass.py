import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime
from datetime import time
from datetime import timedelta
import csv
import matplotlib.ticker as ticker

def scatterPlot(flarelist,sxrlist,hxrlist,title,xlab,ylab,saveas):
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    xdone = 0
    mdone = 0
    cdone = 0
    for i in range(len(sxrlist)):
        if flarelist[i][0] == 'X':
            if xdone == 0:
                plt.scatter(sxrlist[i],hxrlist[i],color = 'blue',label = 'X Class')
                xdone = 1
            else:
                plt.scatter(sxrlist[i],hxrlist[i],color = 'blue')
        elif flarelist[i][0] == 'M':
            if mdone == 0:
                plt.scatter(sxrlist[i],hxrlist[i],color = 'orange',label = 'M Class')
                mdone = 1
            else:
                plt.scatter(sxrlist[i],hxrlist[i],color = 'orange')
        elif flarelist[i][0] == 'C':
            if cdone == 0:
                plt.scatter(sxrlist[i],hxrlist[i],color = 'green',label = 'C Class')
                cdone = 1
            else:
                plt.scatter(sxrlist[i],hxrlist[i],color = 'green')
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.ylim(65000,155000)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.legend()
    plt.savefig(f'CandAboveColoredIntegralLowerPop{saveas}.png')
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

df = pd.read_csv('CandAboveDifsClsassesIntegrals.csv')

difs18 = df['1.0-8.0A_time_until_peak'].tolist()

difs410 = df['4-10keV_time_until_peak'].tolist()
difs1015 = df['10-15keV_time_until_peak'].tolist()
difs1525 = df['15-25keV_time_until_peak'].tolist()
difs2550 = df['25-50keV_time_until_peak'].tolist()
difs5084 = df['50-84keV_time_until_peak'].tolist()
flareClass = df['flare_class']

int410 = df['4-10keV_3_min_integral'].tolist()
int1015 = df['10-15keV_3_min_integral'].tolist()
int1525 = df['15-25keV_3_min_integral'].tolist()
int2550 = df['25-50keV_3_min_integral'].tolist()
int5084 = df['50-84keV_3_min_integral'].tolist()

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

#scatterPlot(flareClass,difs18,int410,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR 3 Minute Integral (4-10keV) (counts s)','logdifs18int410')
#scatterPlot(flareClass,difs18,int1015,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR 3 Minute Integral (10-15keV) (counts s)','logdifs18int1015')
#scatterPlot(flareClass,difs18,int1525,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR 3 Minute Integral (15-25keV) (counts s)','logdifs18int1525')
scatterPlot(flareClass,difs18,int2550,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR 3 Minute Integral (25-50keV) (counts s)','difs18int2550')
#scatterPlot(flareClass,difs18,int5084,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR 3 Minute Integral (50-84keV) (counts s)','difs18int5084')
