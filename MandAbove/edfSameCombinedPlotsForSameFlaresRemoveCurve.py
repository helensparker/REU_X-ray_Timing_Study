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

df = pd.read_csv('matching_flares.csv')

index = 0
distance = 1
for i in tqdm(range(index,index+distance)):
    start = df.iloc[i,0]
    end = df.iloc[i,1]

    for j in range(17,4,-1):
        result_goes = Fido.search(a.Time(start, end), a.Instrument("XRS"), a.goes.SatelliteNumber(17), a.Resolution("flx1s"))
        coolFile = Fido.fetch(result_goes)
        goes = ts.TimeSeries(coolFile)
        if not type(goes) is list:
            sstart = df.iloc[i,2]
            send = df.iloc[i,3]
            dgstart = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
            dgend = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
            dsstart = datetime.strptime(sstart, "%Y-%m-%dT%H:%M:%S.%f")
            dsend = datetime.strptime(send, "%Y-%m-%dT%H:%M:%S.%f")
            if dgstart < dsstart:
                sstart = start
            if dgend > dsend:
                send = end
            lc = LightCurves.from_sdc(start_utc=sstart, end_utc=send, ltc=False)
            ax1 = lc.peek()
            ax2 = ax1.twinx()
            goes.plot(axes=ax2,columns=["xrsb"])
            #to not remove other curve: goes.plot(axes=ax2)
            ax1.get_legend().remove()
            ax2.get_legend().remove()
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines1 + lines2, labels1 + labels2)
            ax2.set_xlim(sstart, send)

            plt.savefig(f'{i}StixGoesLightCurveRemoval.png')
            break