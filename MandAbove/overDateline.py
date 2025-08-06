import pandas as pd
from datetime import datetime
from tqdm import tqdm

df = pd.read_csv('better_matching_flares.csv')

for i in tqdm(range(1067)):
    start = df.iloc[i,0]
    end = df.iloc[i,1]
    dgstart = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
    dgend = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
    if dgstart.date() != dgend.date():
        print(i)