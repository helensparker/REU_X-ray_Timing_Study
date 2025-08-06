import matplotlib.pyplot as plt
import numpy as np

from astropy.visualization import time_support

from sunpy import timeseries as ts
from sunpy.net import Fido
from sunpy.net import attrs as a
import pandas as pd

i = 26

df = pd.read_csv('better_matching_flares.csv')
start = df.iloc[i,0]
end = df.iloc[i,1]
result = Fido.search(a.Time(start, end), a.Instrument("XRS"))
result_goes = Fido.search(a.Time(start, end), a.Instrument("XRS"), a.goes.SatelliteNumber(17), a.Resolution("flx1s"))
coolFile = Fido.fetch(result_goes)
goes = ts.TimeSeries(coolFile)
goes.peek()