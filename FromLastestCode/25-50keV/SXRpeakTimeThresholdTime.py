import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import statistics

def getToHistogram(flareList, thresholdList, sxrPeaks, title, xlab, saveas):
    difList,flares = timeDifference(thresholdList,sxrPeaks,flareList)
    histogram(flares,difList,title,xlab,saveas)


def timeDifference(thresholdList,sxrPeaks,flareList):
    difList = []
    flares = []
    for i in range(len(thresholdList)):
        if thresholdList[i] != 'nan':
            thTime = datetime.strptime(thresholdList[i], "%Y-%m-%d %H:%M:%S.%f")
            peakTime = datetime.strptime(sxrPeaks[i], "%Y-%m-%d %H:%M:%S")
            difList.append(peakTime - thTime)
            flares.append(flareList[i])
    return convertToSeconds(difList),flares
            

def convertToSeconds(timelist):
    sList = []
    for i in range(len(timelist)):
        realsecs = timelist[i].total_seconds()
        sList.append(realsecs)
    return sList

def histogram(flarelist, timediflist, title, xlab, saveas):

    #print(len(flarelist),len(timediflist))
    data_by_class = {'C': [], 'M': [], 'X': []}

    for flare, timedif in zip(flarelist, timediflist):
        if flare[0] in data_by_class:
            data_by_class[flare[0]].append(timedif)
    data = [data_by_class['C'], data_by_class['M'], data_by_class['X']]
    colors = ['green', 'orange', 'blue']
    labels = [f'C Class: {len(data_by_class['C'])} flares, Median: {statistics.median(data_by_class['C'])}', f'M Class: {len(data_by_class['M'])} flares, Median: {statistics.median(data_by_class['M'])}', f'X Class: {len(data_by_class['X'])} flares, Median: {statistics.median(data_by_class['X'])}']
    plt.hist(data, bins=50, stacked=True, color=colors, label=labels)
    plt.title(title+f': {len(timediflist)} flares, Median: {statistics.median(timediflist)}')
    plt.xlabel(xlab)
    plt.ylabel('Flares')
    plt.legend(loc='upper left')
    plt.savefig(f'LTCHistogram{saveas}.png')
    plt.clf()

df = pd.read_csv('integral.csv')

th1 = df['5.38*10^3_time'].astype(str).tolist()
th2 = df['5.60*10^4_time'].astype(str).tolist()
th3 = df['1.05*10^5_time'].astype(str).tolist()
classes = df['flare_class'].astype(str).tolist()
sxrPeaks = df['1.0-8.0A_peak_time'].astype(str).tolist()

getToHistogram(classes,th1,sxrPeaks,'SXR Peak - HXR Integral Times','Time Difference (25-50 keV) (Threshold: 5.38×10$^3$)(s)','1hist')
getToHistogram(classes,th2,sxrPeaks,'SXR Peak - HXR Integral Times','Time Difference (25-50 keV) (Threshold: 5.60×10$^4$)(s)','2hist')
getToHistogram(classes,th3,sxrPeaks,'SXR Peak - HXR Integral Times','Time Difference (25-50 keV) (Threshold: 1.05×10$^5$)(s)','3hist')