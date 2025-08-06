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
    #plt.xscale('log')
    #plt.yscale('log')
    plt.legend()
    plt.savefig(f'CandAboveColored{saveas}.png')
    plt.clf()

def histogram(flarelist, timediflist, title, xlab, saveas):
    data_by_class = {'C': [], 'M': [], 'X': []}

    for flare, timedif in zip(flarelist, timediflist):
        if flare[0] in data_by_class:
            data_by_class[flare[0]].append(timedif)
    data = [data_by_class['C'], data_by_class['M'], data_by_class['X']]
    colors = ['green', 'orange', 'blue']
    labels = ['C Class', 'M Class', 'X Class']
    plt.hist(data, bins=25, stacked=True, color=colors, label=labels)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel('Flares')
    plt.legend()
    plt.savefig(f'LTCHistogram{saveas}.png')
    plt.clf()

def difsbetween(hxrlist,sxrlist):
    difsbetlist = []
    for i in range(len(hxrlist)):
        difsbetlist.append(sxrlist[i]-hxrlist[i])
    return difsbetlist


def removeMilisecs(difslist):
    newdifslist = []
    removeindlist = []
    for i in range(len(difslist)):
        newdifslist.append(difslist[i][2:7])
    return [newdifslist,removeindlist]

'''def convertToSeconds(timelist):
    sList = []
    for t in timelist:
        m, s = map(int, t.split(":"))
        realsecs = m * 60 + s
        sList.append(realsecs)
    return sList'''

def convertToSeconds(timelist,peaklist):
    sList = []
    for i in range(len(timelist)):
        if peaklist[i] == 0:
            sList.append(0)
        elif 'day' in timelist[i]:
            sList.append(0)
        else:
            m, s = map(int, timelist[i].split(":"))
            realsecs = m * 60 + s
            sList.append(realsecs)
    return sList

df = pd.read_csv('LTCMPFLFRemoveuselessDifsClasses.csv')

difs18 = df['1.0-8.0A_time_until_peak'].tolist()

difs410 = df['4-10keV_time_until_peak'].tolist()
difs1015 = df['10-15keV_time_until_peak'].tolist()
difs1525 = df['15-25keV_time_until_peak'].tolist()
difs2550 = df['25-50keV_time_until_peak'].tolist()
difs5084 = df['50-84keV_time_until_peak'].tolist()
flareClass = df['flare_class']

ndifs410 = df['4-10keV_smooth_time_until_peak'].tolist()
ndifs1015 = df['10-15keV_smooth_time_until_peak'].tolist()
ndifs1525 = df['15-25keV_smooth_time_until_peak'].tolist()
ndifs2550 = df['25-50keV_smooth_time_until_peak'].tolist()
ndifs5084 = df['50-84keV_smooth_time_until_peak'].tolist()

peaks410 = df['4-10keV_peak_val'].tolist()
peaks1015 = df['10-15keV_peak_val'].tolist()
peaks1525 = df['15-25keV_peak_val'].tolist()
peaks2550 = df['25-50keV_peak_val'].tolist()
peaks5084 = df['50-84keV_peak_val'].tolist()
peaks18 = df['1.0-8.0A_peak_val'].tolist()

alldifs18 = removeMilisecs(difs18)
alldifs410 = removeMilisecs(difs410)
alldifs1015 = removeMilisecs(difs1015)
alldifs1525 = removeMilisecs(difs1525)
alldifs2550 = removeMilisecs(difs2550)
alldifs5084 = removeMilisecs(difs5084)

nalldifs410 = removeMilisecs(ndifs410)
nalldifs1015 = removeMilisecs(ndifs1015)
nalldifs1525 = removeMilisecs(ndifs1525)
nalldifs2550 = removeMilisecs(ndifs2550)
nalldifs5084 = removeMilisecs(ndifs5084)

difs18 = alldifs18[0]
difs410 = alldifs410[0]
difs1015 = alldifs1015[0]
difs1525 = alldifs1525[0]
difs2550 = alldifs2550[0]
difs5084 = alldifs5084[0]

ndifs410 = nalldifs410[0]
ndifs1015 = nalldifs1015[0]
ndifs1525 = nalldifs1525[0]
ndifs2550 = nalldifs2550[0]
ndifs5084 = nalldifs5084[0]

difs18 = convertToSeconds(difs18,peaks18)
difs410 = convertToSeconds(difs410,peaks410)
difs1015 = convertToSeconds(difs1015,peaks1015)
difs1525 = convertToSeconds(difs1525,peaks1525)
difs2550 = convertToSeconds(difs2550,peaks2550)
difs5084 = convertToSeconds(difs5084,peaks5084)

ndifs410 = convertToSeconds(ndifs410,peaks410)
ndifs1015 = convertToSeconds(ndifs1015,peaks1015)
ndifs1525 = convertToSeconds(ndifs1525,peaks1525)
ndifs2550 = convertToSeconds(ndifs2550,peaks2550)
ndifs5084 = convertToSeconds(ndifs5084,peaks5084)

difbetween410 = difsbetween(difs410,difs18)
difbetween1015 = difsbetween(difs1015,difs18)
difbetween1525 = difsbetween(difs1525,difs18)
difbetween2550 = difsbetween(difs2550,difs18)
difbetween5084 = difsbetween(difs5084,difs18)

ndifbetween410 = difsbetween(ndifs410,difs18)
ndifbetween1015 = difsbetween(ndifs1015,difs18)
ndifbetween1525 = difsbetween(ndifs1525,difs18)
ndifbetween2550 = difsbetween(ndifs2550,difs18)
ndifbetween5084 = difsbetween(ndifs5084,difs18)


consTitle = 'SXR - HXR Peak Times'
nconsTitle = 'SXR - HXR Peak Times Smoothed Curves'

for i in ndifbetween5084:
    if i <= 0:
        print(i)
exit()


histogram(flareClass,difbetween410,consTitle,'Time Difference (4-10 keV) (s)','difs410')
histogram(flareClass,difbetween1015,consTitle,'Time Difference (10-15 keV) (s)','difs1015')
histogram(flareClass,difbetween1525,consTitle,'Time Difference (15-25 keV) (s)','difs1525')
histogram(flareClass,difbetween2550,consTitle,'Time Difference (25-50 keV) (s)','difs2550')
histogram(flareClass,difbetween5084,consTitle,'Time Difference (50-84 keV) (s)','difs5084')

histogram(flareClass,ndifbetween410,nconsTitle,'Time Difference (4-10 keV) (s)','smdifs410')
histogram(flareClass,ndifbetween1015,nconsTitle,'Time Difference (10-15 keV) (s)','smdifs1015')
histogram(flareClass,ndifbetween1525,nconsTitle,'Time Difference (15-25 keV) (s)','smdifs1525')
histogram(flareClass,ndifbetween2550,nconsTitle,'Time Difference (25-50 keV) (s)','smdifs2550')
histogram(flareClass,ndifbetween5084,nconsTitle,'Time Difference (50-84 keV) (s)','smdifs5084')


