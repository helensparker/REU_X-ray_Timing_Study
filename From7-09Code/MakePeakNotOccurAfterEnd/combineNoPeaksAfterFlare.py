import pandas as pd
from tqdm import tqdm
from datetime import datetime
import csv

df = pd.read_csv('testREALActualNPAnewTimeDifsTrial.csv')
df2 = pd.read_csv('combinedActualREALNoPeaksAfterFlare.csv')

index = 0
data = []

for i in tqdm(range(4289)):
    if df2.iloc[i,0] == df.iloc[index,0]:
        data.append(df2.iloc[i,0:6].tolist()+df.iloc[index,6:20].tolist()+df2.iloc[i,20:57].tolist())
        if index != 4:
            index += 1
    else:
        data.append(df2.iloc[i].tolist())

with open('NEWcombinedActualREALNoPeaksAfterFlare.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)