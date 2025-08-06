#Adjusted to have visible_from_earth==True, Use XRS start time

import pandas as pd
from tqdm import tqdm
from datetime import datetime
import csv

df = pd.read_csv('CandAboveflareClass.csv')
df2 = pd.read_csv('LTCMorePeaksFixLowFlaresRemoveuselesstimeDifsPeaktimesandVals.csv')

index = 0
fullList = []
for i in tqdm(range(4312)):
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
            realRow = df2.iloc[i].tolist()
            realRow.append(df.iloc[j,2])
            fullList.append(realRow)
            index = j+1
            break
with open('LTCMPFLFRemoveuselessDifsClasses.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(fullList)