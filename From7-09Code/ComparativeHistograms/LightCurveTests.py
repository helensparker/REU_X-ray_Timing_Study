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

df = pd.read_csv('LTCMPFLFNoAttFixPeaks.csv')

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
    return [timeslist, integral]



index = 160
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
            ax1 = lc.peek()
            #dsfakestart = datetime.strptime(lc.data['start_utc'], "%Y-%m-%dT%H:%M:%S.%f")

            #hxrfluence0 = getIntegral(0,dsfakestart,dgstart,dgend)
            #hxrfluence1 = getIntegral(1,dsfakestart,dgstart,dgend)
            #hxrfluence2 = getIntegral(2,dsfakestart,dgstart,dgend)
            #hxrfluence3 = getIntegral(3,dsfakestart,dgstart,dgend)
            #hxrfluence4 = getIntegral(4,dsfakestart,dgstart,dgend)
            #plt.plot(hxrfluence0[0],hxrfluence0[1])
            #plt.plot(hxrfluence1[0],hxrfluence1[1])
            #plt.plot(hxrfluence2[0],hxrfluence2[1])
            #plt.plot(hxrfluence3[0],hxrfluence3[1])
            #plt.plot(hxrfluence4[0],hxrfluence4[1])


            #fig, ax1 = plt.subplots()

           # ax1.plot(hxrfluence0[0],hxrfluence0[1],label = '4-10keV')
           # ax1.plot(hxrfluence1[0],hxrfluence1[1],label = '10-15keV')
           # ax1.plot(hxrfluence2[0],hxrfluence2[1],label = '15-25keV')
          #  ax1.plot(hxrfluence3[0],hxrfluence3[1],label = '25-50keV')
          #  ax1.plot(hxrfluence4[0],hxrfluence4[1],label = '50-84keV')
          #  ax1.legend()
          #  ax1.set_ylabel('Fluence (counts s)')
          #  ax1.set_yscale('log')


            #plt.savefig(f'{i}NeupertEffect{j}.png')
            ax2 = ax1.twinx()
            goes.plot(axes=ax2)
            ax1.get_legend().remove()
            ax2.get_legend().remove()
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines1 + lines2, labels1 + labels2)
            ax2.set_xlim(sstart, send)

            #plt.axvline(x=df.iloc[i,26])
            plt.axvline(x=df.iloc[i,6])

            plt.savefig(f'{i}CombinedLightCurves{j}.png')
            break