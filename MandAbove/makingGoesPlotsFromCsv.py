import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

from astropy.visualization import time_support

from sunpy import timeseries as ts
from sunpy.net import Fido
from sunpy.net import attrs as a

#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
from math import *
#from tqdm import tqdm
from pprint import pprint
from datetime import timedelta
#from matplotlib import pyplot as plt
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

df = pd.read_csv('goes_feb_2021_to_feb_2025_flares')
df2 = pd.read_csv('STIX_flarelist_w_locations_20210214_20250228_version1_python.csv')


dataList = []

#start = df.iloc[1,0]
#end = df.iloc[1,1]
#result = Fido.search(a.Time(start,end), a.Instrument("XRS"))
#result_goes2 = Fido.search(a.Time(start, end), a.Instrument("XRS"), a.goes.SatelliteNumber(2), a.Resolution("flx1s"))
#print(result_goes2)
#exit()


for i in tqdm(range(1,2)):
    start = df.iloc[i,0]
    end = df.iloc[i,1]
    result = Fido.search(a.Time(start,end), a.Instrument("XRS"))

    #result_goes16 = Fido.search(a.Time(start, end), a.Instrument("XRS"), a.goes.SatelliteNumber(10), a.Resolution("flx1s"))
    #dataList.append(result_goes16)
    #coolFile = Fido.fetch(dataList[i-1])
    #goes = ts.TimeSeries(coolFile)
    
    #if not type(goes) is list:
        #goes.plot()
        #plt.savefig(f'{i}GoesLightCurve10.png')

    #exit()
    result_goes = Fido.search(a.Time(start, end), a.Instrument("XRS"), a.goes.SatelliteNumber(17), a.Resolution("flx1s"))
    coolFile = Fido.fetch(result_goes)
    goes = ts.TimeSeries(coolFile)
    if not type(goes) is list:
        sstart = df2.iloc[40,0]
        send = df2.iloc[40,1]
        lc = LightCurves.from_sdc(start_utc=sstart, end_utc=send, ltc=False)
        ax1 = lc.peek()
        ax2 = ax1.twinx()
        goes_truncated = goes.truncate(sstart, send)
        goes_truncated.plot(axes=ax2)
        ax1.get_legend().remove()
        ax2.get_legend().remove()
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2)
        ax2.set_xlim(sstart, send)




        plt.savefig(f'{i}8GoesLightCurve{17}.png')

        exit()
        
        
        dataList.append(result_goes)
      
        
        start = df2.iloc[40,0]
        end = df2.iloc[40,1]
        lc = LightCurves.from_sdc(start_utc=start, end_utc=end, ltc=True)
        ax = lc.peek()
        #ax.plot()
        trunc = goes.truncate(stixstart,stixend)
        trunc.plot()

        #print(type(ax))
    
        #ax.figure.savefig(f'{i}LightCurve1.png')

        plt.savefig(f'{i}3GoesLightCurve{17}.png')
        exit()
    for j in range(5,19):
        result_goes = Fido.search(a.Time(start, end), a.Instrument("XRS"), a.goes.SatelliteNumber(j), a.Resolution("flx1s"))
        coolFile = Fido.fetch(result_goes)
        goes = ts.TimeSeries(coolFile)
        if not type(goes) is list:
            goes_flare = goes.truncate(start, end)
            dataList.append(result_goes)
            goes_flare.plot()
            plt.savefig(f'{i}TruncGoesLightCurve{j}.png')
            plt.clf()
    
    # print(result_goes)

    #dataList.append(result_goes16)
    #coolFile = Fido.fetch(dataList[i-1])
    #goes = ts.TimeSeries(coolFile)
    #goes.plot()
    #plt.savefig(f'{i}GoesLightCurve16.png')