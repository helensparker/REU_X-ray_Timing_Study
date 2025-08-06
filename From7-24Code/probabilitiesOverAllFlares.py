import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

def probabilities(hxrintlist,flarelist,peakslist,eRange,peakInt,units):
    newhxrintlist,xhlist,mhlist,chlist = [],[],[],[]

    for i in range(len(hxrintlist)):
        if peakslist[i]>0 and hxrintlist[i]>0:
            newhxrintlist.append(hxrintlist[i])
            if flarelist[i][0] == 'X':
                xhlist.append(hxrintlist[i])
            elif flarelist[i][0] == 'M':
                mhlist.append(hxrintlist[i])
            elif flarelist[i][0] == 'C':
                chlist.append(hxrintlist[i])
    minHxr = min(newhxrintlist)
    maxHxr = max(newhxrintlist)
    hxrintTest = np.logspace(np.log10(minHxr), np.log10(maxHxr), num=10001)
    hxrintTest = hxrintTest.tolist()
    del hxrintTest[-1]
    '''hxrintTest = [minHxr]
    num = 1000
    toInc = (maxHxr-minHxr)/num
    for i in range(num-1):
        hxrintTest.append(hxrintTest[-1]+toInc)'''

    probC,probM,probX = [],[],[]
    percC,percM,percX = [],[],[]
    done = False
    for i in tqdm(range(len(hxrintTest))):
        cCount = getNumAbove(chlist,hxrintTest[i])
        mCount = getNumAbove(mhlist,hxrintTest[i])
        xCount = getNumAbove(xhlist,hxrintTest[i])
        allCount = getNumAbove(hxrintlist,hxrintTest[i])
        if xCount/allCount > 0.80 and done == False:
            done = True
            print(hxrintTest[i],cCount/allCount,mCount/allCount,xCount/allCount)
        probC.append(cCount/allCount)
        probM.append(mCount/allCount)
        probX.append(xCount/allCount)

        allC = 3549
        allM = 689
        allX = 41

        percC.append(cCount/allC*100)
        percM.append(mCount/allM*100)
        percX.append(xCount/allX*100)
        '''
    plt.plot(hxrintTest,probC,color='green',label='C Class')
    plt.plot(hxrintTest,probM,color='orange',label='M Class')
    plt.plot(hxrintTest,probX,color='blue',label='X Class')
    plt.xlim(minHxr,maxHxr)
    plt.xscale('log')
    plt.legend()
    plt.title(f'Probability of Class Given HXR {peakInt} is at Least')
    plt.xlabel(f'HXR {peakInt} ({eRange} keV) ({units})')
    plt.ylabel('Probability')
    plt.savefig(f'{peakInt}{eRange}prob.png')
    plt.clf()
    '''
    return
    plt.plot(hxrintTest,percC,color='green',label='C Class')
    plt.plot(hxrintTest,percM,color='orange',label='M Class')
    plt.plot(hxrintTest,percX,color='blue',label='X Class')
    plt.xlim(minHxr,maxHxr)
    plt.xscale('log')
    plt.legend()
    plt.title(f'Percent of Flares Included By Class Given HXR {peakInt} is at Least')
    plt.xlabel(f'HXR {peakInt} ({eRange} keV) ({units})')
    plt.ylabel('Percent')
    plt.savefig(f'{peakInt}{eRange}percOverAllFlares.png')
    plt.clf()

def getNumAbove(hxrInt,val):
    counter = 0
    for i in range(len(hxrInt)):
        if hxrInt[i] >= val:
            counter +=1
    return counter

df = pd.read_csv('integralIncludedBunchaData.csv')

ints410 = df['4-10keV_integral_before_peak'].tolist()
ints1015 = df['10-15keV_integral_before_peak'].tolist()
ints1525 = df['15-25keV_integral_before_peak'].tolist()
ints2550 = df['25-50keV_integral_before_peak'].tolist()
ints5084 = df['50-84keV_integral_before_peak'].tolist()

peaks410 = df['4-10keV_peak_val'].tolist()
peaks1015 = df['10-15keV_peak_val'].tolist()
peaks1525 = df['15-25keV_peak_val'].tolist()
peaks2550 = df['25-50keV_peak_val'].tolist()
peaks5084 = df['50-84keV_peak_val'].tolist()

flareClass = df['flare_class']
'''
probabilities(ints410,flareClass,peaks410,'4-10','Integral','Counts s')
probabilities(ints1015,flareClass,peaks1015,'10-15','Integral','Counts s')
probabilities(ints1525,flareClass,peaks1525,'15-25','Integral','Counts s')
'''

probabilities(ints2550,flareClass,peaks2550,'25-50','Integral','Counts s')
exit()
probabilities(ints5084,flareClass,peaks5084,'50-84','Integral','Counts s')

probabilities(peaks410,flareClass,peaks410,'4-10','Peak','Counts')
probabilities(peaks1015,flareClass,peaks1015,'10-15','Peak','Counts')
probabilities(peaks1525,flareClass,peaks1525,'15-25','Peak','Counts')
probabilities(peaks2550,flareClass,peaks2550,'25-50','Peak','Counts')
probabilities(peaks5084,flareClass,peaks5084,'50-84','Peak','Counts')