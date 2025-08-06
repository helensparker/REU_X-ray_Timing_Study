import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from datetime import time
from datetime import timedelta
import csv

def toDatetime(ortime):
    if ortime[10]=='T':
        newtime = datetime.strptime(ortime, "%Y-%m-%dT%H:%M:%S.%f")
    elif len(ortime) == 19:
        newtime = datetime.strptime(ortime, "%Y-%m-%d %H:%M:%S")
    else:
        newtime = datetime.strptime(ortime, "%Y-%m-%d %H:%M:%S.%f")
    return newtime

def timedif(begining,ending):
    dtbegining = toDatetime(begining)
    dtending = toDatetime(ending)
    timedif = dtending - dtbegining
    return timedif

df = pd.read_csv('LTCRemoveuselesspeaktimesandVals.csv')

data = []

for i in tqdm(range(0,4454)):
    start = df.iloc[i,0]
    end = df.iloc[i,1]
    time18 = df.iloc[i,2]
    val18 = df.iloc[i,3]
    time410 = df.iloc[i,4]
    val410 = df.iloc[i,5]
    time1015 = df.iloc[i,6]
    val1015 = df.iloc[i,7]
    time1525 = df.iloc[i,8]
    val1525 = df.iloc[i,9]
    time2550 = df.iloc[i,10]
    val2550 = df.iloc[i,11]
    time5084 = df.iloc[i,12]
    val5084 = df.iloc[i,13]

    if not (val18 == 0):
        duration = timedif(start,end)
        dif18 = timedif(start,time18)
        dif410 = timedif(start,time410)
        dif1015 = timedif(start,time1015)
        dif1525 = timedif(start,time1525)
        dif2550 = timedif(start,time2550)
        dif5084 = timedif(start,time5084)

        data.append([start,end,duration,time18,dif18,val18,time410,dif410,val410,time1015,dif1015,val1015,time1525,dif1525,val1525,time2550,dif2550,val2550,time5084,dif5084,val5084])


with open('LTCRemoveuselesstimeDifsPeaktimesandVals.csv', 'w', newline='') as file :
    writer = csv.writer(file)
    writer.writerows(data)