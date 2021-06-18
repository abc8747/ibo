import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import pandas as pd

n = 8

files = os.listdir('output')
for filename in files:
    with open(f'output/{filename}', mode='r+', newline='') as f:
        data = [float(d[1]) for d in list(csv.reader(f))]

        df = pd.DataFrame(data, columns=['data'])
        df['min'] = df.iloc[argrelextrema(df.data.values, np.less_equal, order=n)[0]]['data']
        df = df.dropna()
        print(df)
        df.to_csv(f'output1/{filename}', mode='w+', columns=['min'])