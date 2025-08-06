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

def getIntegralB4peak(c,dsfakestart,dsstart,background,peaktime):
    valueslist = []
    for k in range(len(lc.data['counts'][c])):
        val = lc.data['counts'][c][k]
        if dsfakestart + timedelta(0,lc.data['delta_time'][k]) > peaktime:
            break
        if not dsfakestart + timedelta(0,lc.data['delta_time'][k]) < dsstart:
            valueslist.append(val-background)
    if valueslist ==[]:
        return 0
    return sum(valueslist)

df = pd.read_csv('NEWcombinedActualREALNoPeaksAfterFlare.csv')

index = 3+13+1+4+10+6+13+3+1+2+1+6+13+1+1+1+1+2+10+2+1+2+1+9+10+1+2+1+1+3+2+3+1+3+1+8+5+2+1+1+7+1+3+3+1+3+4+1+2+1+1+1+2+2+5+1+3+2+3+1+9
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
        #print(df.iloc[i,6])
        integral410 = getIntegralB4peak(0,dsfakestart,dsstart,df.iloc[i,21],datetime.strptime(df.iloc[i,6], "%Y-%m-%d %H:%M:%S.%f"))

        integral1015 = getIntegralB4peak(1,dsfakestart,dsstart,df.iloc[i,22],datetime.strptime(df.iloc[i,9], "%Y-%m-%d %H:%M:%S.%f"))

        integral1525 = getIntegralB4peak(2,dsfakestart,dsstart,df.iloc[i,23],datetime.strptime(df.iloc[i,12], "%Y-%m-%d %H:%M:%S.%f"))

        integral2550 = getIntegralB4peak(3,dsfakestart,dsstart,df.iloc[i,24],datetime.strptime(df.iloc[i,15], "%Y-%m-%d %H:%M:%S.%f"))

        integral5084 = getIntegralB4peak(4,dsfakestart,dsstart,df.iloc[i,25],datetime.strptime(df.iloc[i,18], "%Y-%m-%d %H:%M:%S.%f"))

        row = df.iloc[i].tolist()
        del row[-1]
        row.extend([integral410,integral1015,integral1525,integral2550,integral5084])
        writer.writerow(row)