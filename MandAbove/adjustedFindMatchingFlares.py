#Adjusted to have visible_from_earth==True, Use XRS start time

import pandas as pd
from tqdm import tqdm
from datetime import datetime
import csv

df = pd.read_csv('classCandAbovegoes_feb_2021_to_feb_2025_flares.csv')
df2 = pd.read_csv('STIX_flarelist_w_locations_20210214_20250228_version1_python.csv')

index = 0
matchingFlares = []
for i in tqdm(range(9782)):
    gstart = df.iloc[i,0]
    gend = df.iloc[i,1]
    for j in tqdm(range(index,25218)):
        sstart = df2.iloc[j,0]
        send = df2.iloc[j,1]
        visFromEarth = df2.iloc[j,19]
        dgstart = datetime.strptime(gstart, "%Y-%m-%d %H:%M:%S.%f")
        dgend = datetime.strptime(gend, "%Y-%m-%d %H:%M:%S.%f")
        dsstart = datetime.strptime(sstart, "%Y-%m-%dT%H:%M:%S.%f")
        dsend = datetime.strptime(send, "%Y-%m-%dT%H:%M:%S.%f")
        startdif = dgstart - dsstart

        if startdif.total_seconds() < -86400:
            break
        if abs(startdif.total_seconds()) < 1800 and dgstart < dsend and dsstart < dgend and visFromEarth:
            matchingFlares.append([df.iloc[i,0],df.iloc[i,1],df2.iloc[j,0],df2.iloc[j,1]])
            index = j+1
            break
with open('CandAboveVisfromEarthmatching_flares.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(matchingFlares)