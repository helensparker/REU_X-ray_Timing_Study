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

def peakAfterEnd(ends,peakTimes):
    counter = 0
    indexList = []
    for i in range(len(peakTimes)):
        if peakTimes[i] > ends[i]:
            counter += 1
            indexList.append(i)
    print(counter)
    print(indexList)

def listToDatetime(timelist):
    dateTimelist = []
    for i in range(len(timelist)):
        dateTimelist.append(toDatetime(timelist[i]))
    return dateTimelist

def toDatetime(ortime):
    if ortime[10]=='T':
        newtime = datetime.strptime(ortime, "%Y-%m-%dT%H:%M:%S.%f")
    elif len(ortime) == 19:
        newtime = datetime.strptime(ortime, "%Y-%m-%d %H:%M:%S")
    else:
        newtime = datetime.strptime(ortime, "%Y-%m-%d %H:%M:%S.%f")
    return newtime


#df = pd.read_csv('LTCMPFLFNoAttFixPeaks.csv')
df = pd.read_csv('NEWcombinedActualREALNoPeaksAfterFlare.csv')

endList = df['end_time'].tolist()
timeUntilPeaksgoes = df['1.0-8.0A_peak_time'].tolist()
timeUntilPeaks410 = df['4-10keV_peak_time'].tolist()
timeUntilPeaks1015 = df['10-15keV_peak_time'].tolist()
timeUntilPeaks1525 = df['15-25keV_peak_time'].tolist()
timeUntilPeaks2550 = df['25-50keV_peak_time'].tolist()
timeUntilPeaks5084 = df['50-84keV_peak_time'].tolist()

endList = listToDatetime(endList)
timeUntilPeaksgoes = listToDatetime(timeUntilPeaksgoes)
timeUntilPeaks410 = listToDatetime(timeUntilPeaks410)
timeUntilPeaks1015 = listToDatetime(timeUntilPeaks1015)
timeUntilPeaks1525 = listToDatetime(timeUntilPeaks1525)
timeUntilPeaks2550 = listToDatetime(timeUntilPeaks2550)
timeUntilPeaks5084 = listToDatetime(timeUntilPeaks5084)

peakAfterEnd(endList,timeUntilPeaksgoes)

print('4-10')


peakAfterEnd(endList,timeUntilPeaks410)

print('10-15')
peakAfterEnd(endList,timeUntilPeaks1015)
print('15-25')
peakAfterEnd(endList,timeUntilPeaks1525)
print('25-50')
peakAfterEnd(endList,timeUntilPeaks2550)
print('50-84')
peakAfterEnd(endList,timeUntilPeaks5084)


