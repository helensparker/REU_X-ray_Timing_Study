import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def histogram(timediflist, title, xlab, saveas):
    plt.hist(timediflist, bins=25)
    plt.title(title+f'   Mean: {round(sum(timediflist)/len(timediflist))}')
    plt.xlabel(xlab)
    plt.ylabel('Flares')
    #plt.legend()
    plt.savefig(f'TimeDifHistogram{saveas}.png')
    plt.clf()

def difsbetween(hxrlist,sxrlist):
    difsbetlist = []
    for i in range(len(hxrlist)):
        difsbetlist.append(sxrlist[i]-hxrlist[i])
        if sxrlist[i]-hxrlist[i] > 1000:
            print(i)
    return difsbetlist

df = pd.read_csv('peaksAndSuch.csv')

goesPeaks = df['GOES_peak'].tolist()
tablepeaks = df['BATSE_table_peak'].tolist()
thermalPeaks = df['Thermal_peak'].tolist()
nonThermalPeaks = df['Non-thermal_peak'].tolist()
smoothThermalPeaks = df['Smoothed_Thermal_peak'].tolist()
smoothNonThermalPeaks = df['Smoothed_non-thermal_peak'].tolist()

tablePeakDif = difsbetween(tablepeaks,goesPeaks)
thPeakDif = difsbetween(thermalPeaks,goesPeaks)
nthPeakDif = difsbetween(nonThermalPeaks,goesPeaks)
smthPeakDif = difsbetween(smoothThermalPeaks,goesPeaks)
smnthPeakDif = difsbetween(smoothNonThermalPeaks,goesPeaks)

constitle = 'SXR - HXR Peak'

histogram(tablePeakDif,constitle + ' Based on Table','Time Difference (> 25 keV) (s)','table')
histogram(thPeakDif,constitle,'Time Difference (> 25 keV) (s)','th')
histogram(nthPeakDif,constitle,'Time Difference (> 60 keV) (s)','nth')
histogram(smthPeakDif,constitle + ' Smoothed','Time Difference (> 25 keV) (s)','smth')
histogram(smnthPeakDif,constitle + 'Smoothed','Time Difference (> 60 keV) (s)','smnth')