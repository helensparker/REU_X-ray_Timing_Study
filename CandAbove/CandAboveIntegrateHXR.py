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

def getIntegralFirst3Min(c,dsfakestart,dsstart):
    integral = 0
    for k in range(len(lc.data['counts'][c])):
        val = lc.data['counts'][c][k]
        if dsfakestart + timedelta(0,lc.data['delta_time'][k]) > dsstart + timedelta(0,0,0,0,3,0,0):
            break
        if not dsfakestart + timedelta(0,lc.data['delta_time'][k]) < dsstart:
            integral += 4*val
    return integral

df = pd.read_csv('CandAbovepeaktimesandVals.csv')

index = 3981
#distance = 5
distance = 4507

with open('CandAboveintegrateHXR.csv', 'a', newline='') as file :
    writer = csv.writer(file)
    for i in tqdm(range(index,distance)):
        sstart = df.iloc[i,0]
        send = df.iloc[i,1]
        lc = LightCurves.from_sdc(start_utc=sstart, end_utc=send, ltc=False)
        dsstart = datetime.strptime(sstart, "%Y-%m-%d %H:%M:%S.%f")
        dsend = datetime.strptime(send, "%Y-%m-%d %H:%M:%S.%f")
        dsfakestart = datetime.strptime(lc.data['start_utc'], "%Y-%m-%dT%H:%M:%S.%f")

        integral410 = getIntegralFirst3Min(0,dsfakestart,dsstart)

        integral1015 = getIntegralFirst3Min(1,dsfakestart,dsstart)

        integral1525 = getIntegralFirst3Min(2,dsfakestart,dsstart)

        integral2550 =getIntegralFirst3Min(3,dsfakestart,dsstart)

        integral5084 = getIntegralFirst3Min(4,dsfakestart,dsstart)

        writer.writerow([sstart,send,integral410,integral1015,integral1525,integral2550,integral5084])