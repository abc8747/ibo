import os
import csv
import numpy as np
# import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import pandas as pd

n = 8

files = os.listdir('output')
for filename in files:
    if '180' not in filename:
        continue
    with open(f'output/{filename}', mode='r+', newline='') as f:
        print(filename)

        data = [float(d[1]) for d in list(csv.reader(f))]
        print(data)

        # df = pd.DataFrame(data, columns=['data'])
        # df['min'] = df.iloc[argrelextrema(df.data.values, np.less_equal, order=n)[0]]['data']
        # df = df.dropna()
        # print(df)
        # df.to_csv(f'output1/{filename}', mode='w+', columns=['min'])