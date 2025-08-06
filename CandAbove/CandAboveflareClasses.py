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

df = pd.read_csv('CandAbovepeaktimesandVals.csv')

index = 0
#distance = 5
distance = 1

with open('CandAboveflareClass.csv', 'a', newline='') as file :
    writer = csv.writer(file)
    for i in tqdm(range(index,distance)):
        sstart = df.iloc[i,0]
        send = df.iloc[i,1]

        for j in range(0,1):
            result = Fido.search(a.Time('2021/02/14','2025/02/28'),a.hek.EventType('FL'),a.hek.FL.GOESCls > "C1.0",a.hek.OBS.Observatory == "GOES")
            hek_results = result["hek"]
            filtered_results = hek_results[["event_starttime","event_endtime", "fl_goescls"]]
            for flare in tqdm(filtered_results):
                writer.writerow([flare['event_starttime'],flare['event_endtime'],flare['fl_goescls']])
            break
            result_goes = Fido.search(a.Time(sstart, send), a.Instrument("XRS"), a.goes.SatelliteNumber(j), a.Resolution("flx1s"))
            coolFile = Fido.fetch(result_goes)
            goes = ts.TimeSeries(coolFile)
            if not type(goes) is list:
                dgstart = datetime.strptime(sstart, "%Y-%m-%d %H:%M:%S.%f")
                dgend = datetime.strptime(send, "%Y-%m-%d %H:%M:%S.%f")
                dsstart = dgstart
                dsend = dgend
                truncgoes = goes.truncate(sstart,send)
                arrgoes = truncgoes.to_array()

                flareclass18 = goes['fl_goescls']

                writer.writerow([sstart,send,flareclass18])
                break