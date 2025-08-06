import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime
from datetime import time
from datetime import timedelta
import csv
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm

def scatterPlot(flarelist,sxrlist,hxrlist,title,xlab,ylab,saveas):
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    xdone = 0
    mdone = 0
    cdone = 0
    for i in range(len(sxrlist)):
        if hxrlist[i]==0:
            break
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
'''
def twodHistogram(flarelist,sxrlist,hxrlist,title,xlab,ylab,saveas):
    xslist = []
    xhlist = []
    mslist = []
    mhlist = []
    cslist = []
    chlist = []

    for i in range(len(sxrlist)):
        if flarelist[i][0] == 'X':
            xslist.append(sxrlist[i])
            xhlist.append(hxrlist[i])
        elif flarelist[i][0] == 'M':
            mslist.append(sxrlist[i])
            mhlist.append(hxrlist[i])
        elif flarelist[i][0] == 'C':
            cslist.append(sxrlist[i])
            chlist.append(hxrlist[i])

    plt.hist2d(sxrlist, hxrlist, bins=50, range=None, density=False, weights=None, cmin=None, cmax=None, cmap=plt.cm.nipy_spectral)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.colorbar()
    plt.savefig(f'LTC{saveas}.png')
    plt.clf()

    plt.hist2d(xslist, xhlist, bins=50, range=None, density=False, weights=None, cmin=None, cmax=None, cmap=plt.cm.nipy_spectral)
    plt.title(f'X class {title}')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.colorbar()
    plt.savefig(f'LTCX{saveas}.png')
    plt.clf()

    plt.hist2d(mslist, mhlist, bins=50, range=None, density=False, weights=None, cmin=None, cmax=None, cmap=plt.cm.nipy_spectral)
    plt.title(f'M class {title}')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.colorbar()
    plt.savefig(f'LTCM{saveas}.png')
    plt.clf()

    plt.hist2d(cslist, chlist, bins=50, range=None, density=False, weights=None, cmin=None, cmax=None, cmap=plt.cm.nipy_spectral)
    plt.title(f'C class {title}')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.colorbar()
    plt.savefig(f'LTCC{saveas}.png')
    plt.clf()
'''

def twodHistogram(flarelist,sxrlist,hxrlist,peakslist,title,xlab,ylab,saveas):
    xslist = []
    xhlist = []
    mslist = []
    mhlist = []
    cslist = []
    chlist = []
    newhxrlist = []
    newsxrlist = []
    hxrmin, hxrmax = hxrlist[0], hxrlist[0]
    sxrmin, sxrmax = sxrlist[0], sxrlist[0]
    print(hxrmin)

    for i in range(len(sxrlist)):
        if peakslist[i]!=0 and hxrlist[i]!=0 and sxrlist[i]!=0:
            if sxrlist[i] > sxrmax:
                sxrmax = sxrlist[i]
            if sxrlist[i] < sxrmin and sxrlist[i]!=0:
                sxrmin = sxrlist[i]
            if hxrlist[i] > hxrmax:
                hxrmax = hxrlist[i]
            if hxrlist[i] < hxrmin:
                hxrmin = hxrlist[i]
            if flarelist[i][0] == 'X':
                xslist.append(sxrlist[i])
                xhlist.append(hxrlist[i])
                newsxrlist.append(sxrlist[i])
                newhxrlist.append(hxrlist[i])
            elif flarelist[i][0] == 'M':
                mslist.append(sxrlist[i])
                mhlist.append(hxrlist[i])
                newsxrlist.append(sxrlist[i])
                newhxrlist.append(hxrlist[i])
            elif flarelist[i][0] == 'C':
                cslist.append(sxrlist[i])
                chlist.append(hxrlist[i])
                newsxrlist.append(sxrlist[i])
                newhxrlist.append(hxrlist[i])
    print(hxrmin)

    #xbins = np.logspace(np.log10(sxrmin), np.log10(sxrmax), 100)
    #ybins = np.logspace(np.log10(hxrmin), np.log10(hxrmax), 100)


    plt.hist2d(newsxrlist, newhxrlist, bins=100, range=None, density=False, weights=None, cmin=None, cmax=None, cmap=plt.cm.nipy_spectral,norm=LogNorm())
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.colorbar()
    plt.savefig(f'LTC{saveas}.png')
    plt.clf()

    plt.hist2d(xslist, xhlist, bins=100, range=None, density=False, weights=None, cmin=None, cmax=None, cmap=plt.cm.nipy_spectral,norm=LogNorm())
    plt.title(f'X class {title}')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.colorbar()
    plt.savefig(f'LTCX{saveas}.png')
    plt.clf()

    plt.hist2d(mslist, mhlist, bins=100, range=None, density=False, weights=None, cmin=None, cmax=None, cmap=plt.cm.nipy_spectral,norm=LogNorm())
    plt.title(f'M class {title}')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.colorbar()
    plt.savefig(f'LTCM{saveas}.png')
    plt.clf()

    plt.hist2d(cslist, chlist, bins=100, range=None, density=False, weights=None, cmin=None, cmax=None, cmap=plt.cm.nipy_spectral,norm=LogNorm())
    plt.title(f'C class {title}')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.colorbar()
    plt.savefig(f'LTCC{saveas}.png')
    plt.clf()

def removeMilisecs(difslist):
    newdifslist = []
    removeindlist = []
    for i in range(len(difslist)):
        newdifslist.append(difslist[i][2:7])
    return [newdifslist,removeindlist]

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

flareClass = df['flare_class']

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


consTitle = 'Hard & Soft X-rays Peak Time Since Start of Flare'
nconsTitle = 'Hard & Soft X-rays Peak Time Since Start of Flare Smoothed Curves'

twodHistogram(flareClass,difs18,difs410,peaks410,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (4-10keV) (s)','difs18difs410')
twodHistogram(flareClass,difs18,difs1015,peaks1015,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (10-15keV) (s)','difs18difs1015')
twodHistogram(flareClass,difs18,difs1525,peaks1525,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (15-25keV) (s)','difs18difs1525')
twodHistogram(flareClass,difs18,difs2550,peaks2550,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (25-50keV) (s)','difs18difs2550')
twodHistogram(flareClass,difs18,difs5084,peaks5084,consTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (50-84keV) (s)','difs18difs5084')

twodHistogram(flareClass,difs18,ndifs410,peaks410,nconsTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (4-10keV) (s)','smdifs18difs410')
twodHistogram(flareClass,difs18,ndifs1015,peaks1015,nconsTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (10-15keV) (s)','smdifs18difs1015')
twodHistogram(flareClass,difs18,ndifs1525,peaks1525,nconsTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (15-25keV) (s)','smdifs18difs1525')
twodHistogram(flareClass,difs18,ndifs2550,peaks2550,nconsTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (25-50keV) (s)','smdifs18difs2550')
twodHistogram(flareClass,difs18,ndifs5084,peaks5084,nconsTitle,'SXR Time from Start of Flare (1.0-8.0A) (s)','HXR Time from Start of Flare (50-84keV) (s)','smdifs18difs5084')
