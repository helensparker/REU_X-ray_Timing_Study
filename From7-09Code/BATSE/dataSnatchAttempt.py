from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

triggerNum = 7006

filename = f'discsc_bfits_{triggerNum}.fits'
hdul = fits.open(filename)
header = hdul[0].header
data = hdul[2].data
hdul.close()

def smoothCurve(timeslist,vals):
    smoothedVals = np.convolve(vals,np.ones(15)/15,mode='same')
    return [timeslist,smoothedVals]

def findPeak(timeslist,smoothedVals):
    max = 0
    times = 0
    for i in range(len(smoothedVals)):
        if smoothedVals[i] > max:
            max = smoothedVals[i]
            times = timeslist[i]
    return max, times


timeList = []
counts2560 = []
counts60110 = []
counts110300 = []
countsgt300 = []
sumList = []
nonThermalSumList = []
for i in range(len(data)):
    timeList.append(data[i][0][1])
    counts2560.append(data[i][1][0])
    counts60110.append(data[i][1][1])
    counts110300.append(data[i][1][2])
    countsgt300.append(data[i][1][3])
    sumList.append(data[i][1][0]+data[i][1][1]+data[i][1][2]+data[i][1][3])
    nonThermalSumList.append(data[i][1][1]+data[i][1][2]+data[i][1][3])
plt.axvline(x=63)
plt.axhline(y=13608.7)
plt.axhline(y=34128.48)
plt.plot(timeList,counts2560,label = '25 - 60 keV')
plt.plot(timeList,counts60110,label = '60 - 110 keV')
plt.plot(timeList,counts110300,label = '110 - 300 keV')
plt.plot(timeList,countsgt300,label = '> 300 keV')
#plt.plot([470,470],[0,140000])
plt.yscale('log')
plt.legend()
plt.xlabel('Time Since Trigger (s)')
plt.ylabel('Counts')
plt.title('BATSE Light Curves')
plt.savefig(f'allCurves{triggerNum}')



plt.clf()
smoothedSumList = np.convolve(sumList,np.ones(15)/15,mode='same')
plt.plot(timeList,sumList)
plt.yscale('log')
plt.xlabel('Time Since Trigger (s)')
plt.ylabel('Counts')
plt.axvline(x=findPeak(timeList,sumList)[1])
plt.axvline(x=findPeak(timeList,smoothedSumList)[1],color='red')
plt.savefig(f'sum{triggerNum}')

plt.clf()
ntsmoothedSumList = np.convolve(nonThermalSumList,np.ones(15)/15,mode='same')
plt.plot(timeList,nonThermalSumList)
plt.yscale('log')
plt.xlabel('Time Since Trigger (s)')
plt.ylabel('Counts')
plt.axvline(x=findPeak(timeList,sumList)[1])
plt.axvline(x=findPeak(timeList,nonThermalSumList)[1])
print(findPeak(timeList,sumList)[1],findPeak(timeList,nonThermalSumList)[1],findPeak(timeList,ntsmoothedSumList)[1],findPeak(timeList,smoothedSumList)[1])
plt.savefig(f'nthsum{triggerNum}')

plt.clf()

plt.plot(timeList,smoothedSumList)
plt.yscale('log')
plt.xlabel('Time Since Trigger (s)')
plt.ylabel('Counts')
plt.savefig(f'smsum{triggerNum}')

plt.clf()

plt.plot(timeList,ntsmoothedSumList)
plt.yscale('log')
plt.xlabel('Time Since Trigger (s)')
plt.ylabel('Counts')
plt.savefig(f'ntsmsum{triggerNum}')



#print(data)