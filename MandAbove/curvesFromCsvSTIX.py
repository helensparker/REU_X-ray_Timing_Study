import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import *
from tqdm import tqdm
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
#from google.colab import data_table
#data_table.enable_dataframe_formatter()





df = pd.read_csv('STIX_flarelist_w_locations_20210214_20250228_version1_python.csv')



for i in tqdm(range(40,41)):
    start = df.iloc[i,0]
    end = df.iloc[i,1]
    lc = LightCurves.from_sdc(start_utc=start, end_utc=end, ltc=True)
    fig=lc.peek()
    fig.figure.savefig(f'{i}LightCurve1.png')
    lc.data.keys()