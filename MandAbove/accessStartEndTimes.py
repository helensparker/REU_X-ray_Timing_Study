import pandas as pd
import matplotlib.pyplot as plt
from math import *
from tqdm import tqdm

df = pd.read_csv('STIX_flarelist_w_locations_20210214_20250228_version1_python.csv')


#for i in tqdm(range(2,11)):
for i in range(1,11):
    start = df.iloc[i,0]
    end = df.iloc[i,1]

    print(start,end)