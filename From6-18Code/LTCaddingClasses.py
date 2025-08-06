#Adjusted to have visible_from_earth==True, Use XRS start time

import pandas as pd
from tqdm import tqdm
from datetime import datetime
import csv

df = pd.read_csv('CandAboveflareClass.csv')
df2 = pd.read_csv('LTCtimeDifsPeaktimesandVals.csv')

index = 0
fullList = []
for i in tqdm(range(4371)):
    start = df2.iloc[i,0]
    end = df2.iloc[i,1]
    for j in tqdm(range(index,9782)):
        sstart = df.iloc[j,0]
        send = df.iloc[j,1]
        dgstart = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
        dgend = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
        dsstart = datetime.strptime(sstart, "%Y-%m-%d %H:%M:%S.%f")
        dsend = datetime.strptime(send, "%Y-%m-%d %H:%M:%S.%f")
        startdif = dgstart - dsstart

        if startdif.total_seconds() < -86400:
            break
        if start == sstart:
            fullList.append([df2.iloc[i,0],df2.iloc[i,1],df2.iloc[i,2],df2.iloc[i,3],df2.iloc[i,4],df2.iloc[i,5],df2.iloc[i,6],df2.iloc[i,7],df2.iloc[i,8],df2.iloc[i,9],df2.iloc[i,10],df2.iloc[i,11],df2.iloc[i,12],df2.iloc[i,13],df2.iloc[i,14],df2.iloc[i,15],df2.iloc[i,16],df2.iloc[i,17],df2.iloc[i,18],df2.iloc[i,19],df2.iloc[i,20],df.iloc[j,2]])
            index = j+1
            break
with open('LTCDifsClasses.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(fullList)