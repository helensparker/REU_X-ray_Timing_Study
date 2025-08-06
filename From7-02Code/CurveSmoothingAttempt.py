import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import integrate

from astropy.visualization import time_support

from sunpy import timeseries as ts
from sunpy.net import Fido
from sunpy.net import attrs as a

from math import *
from pprint import pprint
from datetime import timedelta
from astropy.table import QTable
from stixdcpy.quicklook import LightCurves
from stixdcpy.energylut import EnergyLUT
from stixdcpy import auxiliary as aux
from stixdcpy.net import FitsQuery as fq
from stixdcpy.net import Request as jreq
from stixdcpy import instrument as inst
from stixdcpy.science import PixelData, Spectrogram, spec_fits_crop, spec_fits_concatenate, fits_time_to_datetime
from stixdcpy.housekeeping import Housekeeping
from astropy.io import fits
from stixdcpy import detector_view as dv
from stixdcpy import spectrogram  as cspec
from stixdcpy.imgspec import ImgSpecArchive as isar
from datetime import datetime

df = pd.read_csv('LTCMPFLFRemoveuselessDifsClasses.csv')

def getIntegral(c, dsfakestart, dsstart, dgend):
    valueslist = []
    timeslist = []
    inttimelist = []
    for k in range(len(lc.data['counts'][c])):
        val = lc.data['counts'][c][k]
        if dsfakestart + timedelta(0,lc.data['delta_time'][k]) > dgend:
            break
        if not dsfakestart + timedelta(0,lc.data['delta_time'][k]) < dsstart:
            valueslist.append(val)
            timeslist.append(dsfakestart + timedelta(0,lc.data['delta_time'][k]))
            inttimelist.append(lc.data['delta_time'][k])
    integral = integrate.cumulative_trapezoid(valueslist, inttimelist, initial=0)
    return [timeslist, integral,valueslist]
'''
def smoothCurve(c,dsfakestart,dgend,background,peak):
    valueslist = []
    timeslist = []
    inttimelist = []
    for k in range(len(lc.data['counts'][c])):
        val = lc.data['counts'][c][k]
        if dsfakestart + timedelta(0,lc.data['delta_time'][k]) > dgend:
            break
        #if not dsfakestart + timedelta(0,lc.data['delta_time'][k]) < dsstart:
        else:
            valueslist.append(val-background)
            timeslist.append(dsfakestart + timedelta(0,lc.data['delta_time'][k]))
            inttimelist.append(lc.data['delta_time'][k])
    ''''''avgValList = [(valueslist[0]+valueslist[1])/2]
    for i in range(1,len(valueslist)-1):
        if peak == 0:
            avgValList.append(1)
        else:
            avgValList.append((valueslist[i-1]+valueslist[i]+valueslist[i+1])/3)
    avgValList.append((valueslist[-1]+valueslist[-2])/2)''''''

    smoothedVals = np.convolve(valueslist,np.ones(15)/15,mode='same')


    return [timeslist, smoothedVals]
'''

def smoothCurve(timeslist,vals,background):
    newvals = []
    for i in vals:
        newvals.append(i-background)
    for i in range(len(newvals)):
        if newvals[i] < 1:
            newvals[i] = 1
    smoothedVals = np.convolve(newvals,np.ones(15)/15,mode='same')
    return [timeslist,smoothedVals]

def fixAttenuator(hxrfluence,c):
    fixedList = []
    if c == 0:
        bigrange, smallrange = 1000000,800000
    elif c == 1:
        bigrange, smallrange = 100000,100000
    elif c ==2:
        bigrange, smallrange = 9000,6000
    else:
        return hxrfluence[2]
    big = 0
    small = 1
    pos = False
    for m in range(1,len(hxrfluence[2])):
        if abs(hxrfluence[2][m-1] - hxrfluence[2][m]) > bigrange and (hxrfluence[2][m-1] - hxrfluence[2][m] > 0 or pos == True):
            pos = True
            big = hxrfluence[2][m-1]
            small = hxrfluence[2][m+1]
            break
    for p in hxrfluence[2]:
        fixedList.append(p*big/small)
    
    fullList = [hxrfluence[2][0]]
    original = True
    neworiginal = True
    for n in range(1,len(hxrfluence[2])):
        if abs(hxrfluence[2][n-1] - hxrfluence[2][n]) > smallrange and n >= m:
            if original == True:
                neworiginal = False
            else:
                neworiginal = True
        if original != neworiginal:
            fullList.append(0)
            original = neworiginal
        else:
            if original == True:
                fullList.append(hxrfluence[2][n])
            else:
                fullList.append(fixedList[n])

    for n in range(1,len(fullList)-1):
        if fullList[n] == 0:
            fullList[n] = (fullList[n+1]+fullList[n-1])/2
            '''print(n)
            print(hxrfluence0[2][n-1],hxrfluence0[2][n],hxrfluence0[2][n+1])
            print(fullList[n-1],fullList[n],fullList[n+1])'''
    return fullList




index = 440
distance = 1
for i in tqdm(range(index,index+distance)):
    start = df.iloc[i,0]
    end = df.iloc[i,1]

    for j in range(16,4,-1):
        result_goes = Fido.search(a.Time(start, end), a.Instrument("XRS"), a.goes.SatelliteNumber(j), a.Resolution("flx1s"))
        coolFile = Fido.fetch(result_goes)
        goes = ts.TimeSeries(coolFile)
        if not type(goes) is list:
            dgstart = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
            dgend = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
            sstart = start
            send = end
            lc = LightCurves.from_sdc(start_utc=sstart, end_utc=send, ltc=True)
            #ax1 = lc.peek()
            dsfakestart = datetime.strptime(lc.data['start_utc'], "%Y-%m-%dT%H:%M:%S.%f")

            hxrfluence0 = getIntegral(0,dsfakestart,dgstart,dgend)
            hxrfluence1 = getIntegral(1,dsfakestart,dgstart,dgend)
            hxrfluence2 = getIntegral(2,dsfakestart,dgstart,dgend)
            hxrfluence3 = getIntegral(3,dsfakestart,dgstart,dgend)
            hxrfluence4 = getIntegral(4,dsfakestart,dgstart,dgend)

            correctedLC0 = fixAttenuator(hxrfluence0,0)
            correctedLC1 = fixAttenuator(hxrfluence1,1)
            correctedLC2 = fixAttenuator(hxrfluence2,2)
            correctedLC3 = fixAttenuator(hxrfluence3,3)
            correctedLC4 = fixAttenuator(hxrfluence4,4)

            smooth0 = smoothCurve(hxrfluence0[0],correctedLC0,df.iloc[i,21])
            smooth1 = smoothCurve(hxrfluence1[0],correctedLC1,df.iloc[i,22])
            smooth2 = smoothCurve(hxrfluence2[0],correctedLC2,df.iloc[i,23])
            smooth3 = smoothCurve(hxrfluence3[0],correctedLC3,df.iloc[i,24])
            smooth4 = smoothCurve(hxrfluence4[0],correctedLC4,df.iloc[i,25])
            #plt.plot(hxrfluence0[0],hxrfluence0[1])
            #plt.plot(hxrfluence1[0],hxrfluence1[1])
            #plt.plot(hxrfluence2[0],hxrfluence2[1])
            #plt.plot(hxrfluence3[0],hxrfluence3[1])
            #plt.plot(hxrfluence4[0],hxrfluence4[1])


            fig, ax1 = plt.subplots()


            ax1.plot(smooth0[0],smooth0[1],label = '4-10keV')
            ax1.plot(smooth1[0],smooth1[1],label = '10-15keV')
            ax1.plot(smooth2[0],smooth2[1],label = '15-25keV')
            ax1.plot(smooth3[0],smooth3[1],label = '25-50keV')
            ax1.plot(smooth4[0],smooth4[1],label = '50-84keV')
            ax1.legend()
            ax1.set_ylabel('Counts')
            ax1.set_yscale('log')


            #plt.savefig(f'{i}NeupertEffect{j}.png')
            ax2 = ax1.twinx()
            goes.plot(axes=ax2)
            ax1.get_legend().remove()
            ax2.get_legend().remove()
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines1 + lines2, labels1 + labels2)
            ax2.set_xlim(sstart, send)

            plt.savefig(f'{i}SmoothedNoBackNewCurves{j}.png')
            break