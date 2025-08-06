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

    print(len(flarelist),len(timediflist))
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
        
        if hxrlist[i] != -100 and sxrlist[i] != -100:
            difsbetlist.append(sxrlist[i]-hxrlist[i])
        else:
            difsbetlist.append(-100)
        #if sxrlist[i]-hxrlist[i] > 2000:
            #print(i)
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
            sList.append(-100)
        elif 'day' in timelist[i]:
            sList.append(-100)
        else:
            m, s = map(int, timelist[i].split(":"))
            realsecs = m * 60 + s
            sList.append(realsecs)
    return sList

def removal(cuteList,flares):
    cuterList = []
    newFlares = []
    for i in range(len(cuteList)):
        if cuteList[i] != -100:
            cuterList.append(cuteList[i])
            newFlares.append(flares[i])
    return cuterList,newFlares

df = pd.read_csv('LTCMPFLFNoAttFixPeaks.csv')

difs18 = df['1.0-8.0A_time_until_peak'].tolist()

difs410 = df['4-10keV_time_until_peak'].tolist()
difs1015 = df['10-15keV_time_until_peak'].tolist()
difs1525 = df['15-25keV_time_until_peak'].tolist()
difs2550 = df['25-50keV_time_until_peak'].tolist()
difs5084 = df['50-84keV_time_until_peak'].tolist()
flareClass = df['flare_class']

ndifs410 = df['4-10keV_no_att_smooth_time_until_peak'].tolist()
ndifs1015 = df['10-15keV_no_att_smooth_time_until_peak'].tolist()
ndifs1525 = df['15-25keV_no_att_smooth_time_until_peak'].tolist()
ndifs2550 = df['25-50keV_no_att_smooth_time_until_peak'].tolist()
ndifs5084 = df['50-84keV_no_att_smooth_time_until_peak'].tolist()

smdifs410 = df['4-10keV_smooth_time_until_peak'].tolist()
smdifs1015 = df['10-15keV_smooth_time_until_peak'].tolist()
smdifs1525 = df['15-25keV_smooth_time_until_peak'].tolist()
smdifs2550 = df['25-50keV_smooth_time_until_peak'].tolist()
smdifs5084 = df['50-84keV_smooth_time_until_peak'].tolist()

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

smalldifs410 = removeMilisecs(smdifs410)
smalldifs1015 = removeMilisecs(smdifs1015)
smalldifs1525 = removeMilisecs(smdifs1525)
smalldifs2550 = removeMilisecs(smdifs2550)
smalldifs5084 = removeMilisecs(smdifs5084)

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

smdifs410 = smalldifs410[0]
smdifs1015 = smalldifs1015[0]
smdifs1525 = smalldifs1525[0]
smdifs2550 = smalldifs2550[0]
smdifs5084 = smalldifs5084[0]

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

smdifs410 = convertToSeconds(smdifs410,peaks410)
smdifs1015 = convertToSeconds(smdifs1015,peaks1015)
smdifs1525 = convertToSeconds(smdifs1525,peaks1525)
smdifs2550 = convertToSeconds(smdifs2550,peaks2550)
smdifs5084 = convertToSeconds(smdifs5084,peaks5084)

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

smdifbetween410 = difsbetween(smdifs410,difs18)
smdifbetween1015 = difsbetween(smdifs1015,difs18)
smdifbetween1525 = difsbetween(smdifs1525,difs18)
smdifbetween2550 = difsbetween(smdifs2550,difs18)
smdifbetween5084 = difsbetween(smdifs5084,difs18)


consTitle = 'SXR - HXR Peak Times'
nconsTitle = 'SXR - HXR Peak Times Attenuator Corrected'
smconsTitle = 'SXR - HXR Peak Times Smoothed Curves'

'''
for i in ndifbetween5084:
    if i <= 0:
        print(i)
#exit()'''






smoothMinusOrig410 = difsbetween(difbetween410,smdifbetween410)
smoothMinusOrig1015 = difsbetween(difbetween1015,smdifbetween1015)
smoothMinusOrig1525 = difsbetween(difbetween1525,smdifbetween1525)
smoothMinusOrig2550 = difsbetween(difbetween2550,smdifbetween2550)
smoothMinusOrig5084 = difsbetween(difbetween5084,smdifbetween5084)


attMinusOrig410 = difsbetween(difbetween410,ndifbetween410)
attMinusOrig1015 = difsbetween(difbetween1015,ndifbetween1015)
attMinusOrig1525 = difsbetween(difbetween1525,ndifbetween1525)
attMinusOrig2550 = difsbetween(difbetween2550,ndifbetween2550)
attMinusOrig5084 = difsbetween(difbetween5084,ndifbetween5084)


attMinusSmooth410 = difsbetween(smdifbetween410,ndifbetween410)
attMinusSmooth1015 = difsbetween(smdifbetween1015,ndifbetween1015)
attMinusSmooth1525 = difsbetween(smdifbetween1525,ndifbetween1525)
attMinusSmooth2550 = difsbetween(smdifbetween2550,ndifbetween2550)
attMinusSmooth5084 = difsbetween(smdifbetween5084,ndifbetween5084)


sotitle = 'Smooth - Original Peak Times'
aotitle = 'Attenuator Correncted - Original Peak Times'
astitle = 'Attenuator Correncted - Smooth Peak Times'

difbetween410,fldifbetween410 = removal(difbetween410,flareClass)
difbetween1015,fldifbetween1015 = removal(difbetween1015,flareClass)
difbetween1525,fldifbetween1525 = removal(difbetween1525,flareClass)
difbetween2550,fldifbetween2550 = removal(difbetween2550,flareClass)
difbetween5084,fldifbetween5084 = removal(difbetween5084,flareClass)

ndifbetween410,flndifbetween410 = removal(ndifbetween410,flareClass)
ndifbetween1015,flndifbetween1015 = removal(ndifbetween1015,flareClass)
ndifbetween1525,flndifbetween1525 = removal(ndifbetween1525,flareClass)
ndifbetween2550,flndifbetween2550 = removal(ndifbetween2550,flareClass)
ndifbetween5084,flndifbetween5084 = removal(ndifbetween5084,flareClass)

smdifbetween410,flsmdifbetween410 = removal(smdifbetween410,flareClass)
smdifbetween1015,flsmdifbetween1015 = removal(smdifbetween1015,flareClass)
smdifbetween1525,flsmdifbetween1525 = removal(smdifbetween1525,flareClass)
smdifbetween2550,flsmdifbetween2550 = removal(smdifbetween2550,flareClass)
smdifbetween5084,flsmdifbetween5084 = removal(smdifbetween5084,flareClass)

smoothMinusOrig410,flsmoothMinusOrig410 = removal(smoothMinusOrig410,flareClass)
smoothMinusOrig1015,flsmoothMinusOrig1015 = removal(smoothMinusOrig1015,flareClass)
smoothMinusOrig1525,flsmoothMinusOrig1525 = removal(smoothMinusOrig1525,flareClass)
smoothMinusOrig2550,flsmoothMinusOrig2550 = removal(smoothMinusOrig2550,flareClass)
smoothMinusOrig5084,flsmoothMinusOrig5084 = removal(smoothMinusOrig5084,flareClass)

attMinusOrig410,flattMinusOrig410 = removal(attMinusOrig410,flareClass)
attMinusOrig1015,flattMinusOrig1015 = removal(attMinusOrig1015,flareClass)
attMinusOrig1525,flattMinusOrig1525 = removal(attMinusOrig1525,flareClass)
attMinusOrig2550,flattMinusOrig2550 = removal(attMinusOrig2550,flareClass)
attMinusOrig5084,flattMinusOrig5084 = removal(attMinusOrig5084,flareClass)

attMinusSmooth410,flattMinusSmooth410 = removal(attMinusSmooth410,flareClass)
attMinusSmooth1015,flattMinusSmooth1015 = removal(attMinusSmooth1015,flareClass)
attMinusSmooth1525,flattMinusSmooth1525 = removal(attMinusSmooth1525,flareClass)
attMinusSmooth2550,flattMinusSmooth2550 = removal(attMinusSmooth2550,flareClass)
attMinusSmooth5084,flattMinusSmooth5084 = removal(attMinusSmooth5084,flareClass)




histogram(fldifbetween410,difbetween410,consTitle,'Time Difference (4-10 keV) (s)','difs410')
histogram(fldifbetween1015,difbetween1015,consTitle,'Time Difference (10-15 keV) (s)','difs1015')
histogram(fldifbetween1525,difbetween1525,consTitle,'Time Difference (15-25 keV) (s)','difs1525')
histogram(fldifbetween2550,difbetween2550,consTitle,'Time Difference (25-50 keV) (s)','difs2550')
histogram(fldifbetween5084,difbetween5084,consTitle,'Time Difference (50-84 keV) (s)','difs5084')

histogram(flndifbetween410,ndifbetween410,nconsTitle,'Time Difference (4-10 keV) (s)','attsmdifs410')
histogram(flndifbetween1015,ndifbetween1015,nconsTitle,'Time Difference (10-15 keV) (s)','attsmdifs1015')
histogram(flndifbetween1525,ndifbetween1525,nconsTitle,'Time Difference (15-25 keV) (s)','attsmdifs1525')
histogram(flndifbetween2550,ndifbetween2550,nconsTitle,'Time Difference (25-50 keV) (s)','attsmdifs2550')
histogram(flndifbetween5084,ndifbetween5084,nconsTitle,'Time Difference (50-84 keV) (s)','attsmdifs5084')

histogram(flsmdifbetween410,smdifbetween410,smconsTitle,'Time Difference (4-10 keV) (s)','smdifs410')
histogram(flsmdifbetween1015,smdifbetween1015,smconsTitle,'Time Difference (10-15 keV) (s)','smdifs1015')
histogram(flsmdifbetween1525,smdifbetween1525,smconsTitle,'Time Difference (15-25 keV) (s)','smdifs1525')
histogram(flsmdifbetween2550,smdifbetween2550,smconsTitle,'Time Difference (25-50 keV) (s)','smdifs2550')
histogram(flsmdifbetween5084,smdifbetween5084,smconsTitle,'Time Difference (50-84 keV) (s)','smdifs5084')





histogram(flsmoothMinusOrig410,smoothMinusOrig410,sotitle,'Time Difference (4-10 keV) (s)','smOrig410')
histogram(flsmoothMinusOrig1015,smoothMinusOrig1015,sotitle,'Time Difference (10-15 keV) (s)','smOrig1015')
histogram(flsmoothMinusOrig1525,smoothMinusOrig1525,sotitle,'Time Difference (15-25 keV) (s)','smOrig1525')
histogram(flsmoothMinusOrig2550,smoothMinusOrig2550,sotitle,'Time Difference (25-50 keV) (s)','smOrig2550')
histogram(flsmoothMinusOrig5084,smoothMinusOrig5084,sotitle,'Time Difference (50-84 keV) (s)','smOrig5084')

histogram(flattMinusOrig410,attMinusOrig410,aotitle,'Time Difference (4-10 keV) (s)','attOrig410')
histogram(flattMinusOrig1015,attMinusOrig1015,aotitle,'Time Difference (10-15 keV) (s)','attOrig1015')
histogram(flattMinusOrig1525,attMinusOrig1525,aotitle,'Time Difference (15-25 keV) (s)','attOrig1525')
histogram(flattMinusOrig2550,attMinusOrig2550,aotitle,'Time Difference (25-50 keV) (s)','attOrig2550')
histogram(flattMinusOrig5084,attMinusOrig5084,aotitle,'Time Difference (50-84 keV) (s)','attOrig5084')

histogram(flattMinusSmooth410,attMinusSmooth410,astitle,'Time Difference (4-10 keV) (s)','attSm410')
histogram(flattMinusSmooth1015,attMinusSmooth1015,astitle,'Time Difference (10-15 keV) (s)','attSm1015')
histogram(flattMinusSmooth1525,attMinusSmooth1525,astitle,'Time Difference (15-25 keV) (s)','attSm1525')
histogram(flattMinusSmooth2550,attMinusSmooth2550,astitle,'Time Difference (25-50 keV) (s)','attSm2550')
histogram(flattMinusSmooth5084,attMinusSmooth5084,astitle,'Time Difference (50-84 keV) (s)','attSm5084')




