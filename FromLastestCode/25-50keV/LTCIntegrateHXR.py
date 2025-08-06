import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

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
from datetime import time
from datetime import timedelta
import csv
from scipy import integrate

def getTimeIntegralReachesThreshold(c,dsfakestart,dsstart,background,endtime,th1,th2,th3):
    integral = 0
    done1, done2 = False,False
    time1, time2, time3 = 'NA', 'NA', 'NA'
    for i in range(len(lc.data['counts'][c])):
        val = lc.data['counts'][c][i]
        if dsfakestart + timedelta(0,lc.data['delta_time'][i]) > endtime:
            break
        if integral >= th1:
            if done1 == False:
                time1 = dsfakestart + timedelta(0,lc.data['delta_time'][i])
                done1 = True
            if integral >= th2:
                if done2 == False:
                    time2 = dsfakestart + timedelta(0,lc.data['delta_time'][i])
                    done2 = True
                if integral >= th3:
                    time3 = dsfakestart + timedelta(0,lc.data['delta_time'][i])
                    break
        if not dsfakestart + timedelta(0,lc.data['delta_time'][i]) < dsstart:
            integral += val-background
    return time1,time2,time3
    

df = pd.read_csv('NEWcombinedActualREALNoPeaksAfterFlare.csv')

thresholdVal1 = 5.38*10**3
thresholdVal2 = 5.60*10**4
thresholdVal3 = 1.05*10**5

index = 2821
distance = 4289
#distance = 4289

with open('integral.csv', 'a', newline='') as file :
    writer = csv.writer(file)
    for i in tqdm(range(index,distance)):
        sstart = df.iloc[i,0]
        send = df.iloc[i,1]
        lc = LightCurves.from_sdc(start_utc=sstart, end_utc=send, ltc=True)
        dsstart = datetime.strptime(sstart, "%Y-%m-%d %H:%M:%S.%f")
        dsend = datetime.strptime(send, "%Y-%m-%d %H:%M:%S.%f")
        dsfakestart = datetime.strptime(lc.data['start_utc'], "%Y-%m-%dT%H:%M:%S.%f")

        th1time, th2time, th3time = getTimeIntegralReachesThreshold(3,dsfakestart,dsstart,df.iloc[i,24],dsend,thresholdVal1,thresholdVal2,thresholdVal3)

        row = [df.iloc[i,0],df.iloc[i,1],df.iloc[i,3],df.iloc[i,41],th1time,th2time,th3time]
        writer.writerow(row)