#Adjusted to make ltc=True

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


def getMaxandTime(c,dsfakestart,dsstart):
    max = 0
    for k in range(len(lc.data['counts'][c])):
        val = lc.data['counts'][c][k]
        if val > max:
            if not dsfakestart + timedelta(0,lc.data['delta_time'][k]) < dsstart:
                deltatime = lc.data['delta_time'][k]
                max = val
    return [deltatime,max]

def goesGetMaxandTime(array,c):
    max = 0
    deltatime = 0
    for k in range(len(array)):
        val = array[k][c]
        if val > max:
            max = val
            deltatime = k
    return [deltatime,max]
    

df = pd.read_csv('CandAboveVisfromEarthmatching_flares.csv')

data = []

index = 4201
#distance = 5
distance = 4521

with open('LTCpeaktimesandVals.csv', 'a', newline='') as file :
    writer = csv.writer(file)
    for i in tqdm(range(index,distance)):
        start = df.iloc[i,0]
        end = df.iloc[i,1]

        for j in range(17,4,-1):
            result_goes = Fido.search(a.Time(start, end), a.Instrument("XRS"), a.goes.SatelliteNumber(j), a.Resolution("flx1s"))
            coolFile = Fido.fetch(result_goes)
            goes = ts.TimeSeries(coolFile)
            if not type(goes) is list:
                sstart = df.iloc[i,2]
                send = df.iloc[i,3]
                lc = LightCurves.from_sdc(start_utc=sstart, end_utc=send, ltc=True)
                dgstart = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
                dgend = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
                dsstart = datetime.strptime(sstart, "%Y-%m-%dT%H:%M:%S.%f")
                dsend = datetime.strptime(send, "%Y-%m-%dT%H:%M:%S.%f")
                dsfakestart = datetime.strptime(lc.data['start_utc'], "%Y-%m-%dT%H:%M:%S.%f")
                sstart = start
                send = end
                dsstart = dgstart
                dsend = dgend
                truncgoes = goes.truncate(sstart,send)
                arrgoes = truncgoes.to_array()

                maxtime18 = goesGetMaxandTime(arrgoes,1)
                deltatime18 = maxtime18[0]
                time18 = dsstart + timedelta(0,deltatime18)
                val18 = maxtime18[1]

                maxtime410 = getMaxandTime(0,dsfakestart,dsstart)
                deltatime410 = maxtime410[0]
                time410 = dsfakestart + timedelta(0,deltatime410)
                val410 = maxtime410[1]

                maxtime1015 = getMaxandTime(1,dsfakestart,dsstart)
                deltatime1015 = maxtime1015[0]
                time1015 = dsfakestart + timedelta(0,deltatime1015)
                val1015 = maxtime1015[1]

                maxtime1525 = getMaxandTime(2,dsfakestart,dsstart)
                deltatime1525 = maxtime1525[0]
                time1525 = dsfakestart + timedelta(0,deltatime1525)
                val1525 = maxtime1525[1]

                maxtime2550 = getMaxandTime(3,dsfakestart,dsstart)
                deltatime2550 = maxtime2550[0]
                time2550 = dsfakestart + timedelta(0,deltatime2550)
                val2550 = maxtime2550[1]

                maxtime5084 = getMaxandTime(4,dsfakestart,dsstart)
                deltatime5084 = maxtime5084[0]
                time5084 = dsfakestart + timedelta(0,deltatime5084)
                val5084 = maxtime5084[1]

                #data.append([sstart,send,time18,val18,time410,val410,time1015,val1015,time1525,val1525,time2550,val2550,time5084,val5084])
                writer.writerow([sstart,send,time18,val18,time410,val410,time1015,val1015,time1525,val1525,time2550,val2550,time5084,val5084])
                break


#with open('CandAbovepeaktimesandVals.csv', 'w', newline='') as file :
    #writer = csv.writer(file)
    #writer.writerows(data)