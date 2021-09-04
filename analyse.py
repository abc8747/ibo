import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema, find_peaks
import pandas as pd

# def plot_peaks(time, signal, prominence=None):
#     index_data, _ = find_peaks(
#         np.array(signal),
#         prominence=prominence
#     )
#     plt.plot(time, signal)
#     plt.plot(time[index_data[0]], signal[index_data[0]], alpha = 0.5, marker = 'o', mec = 'r',ms = 9, ls = ":",label='%d %s' % (index_data[0].size-1, 'Peaks'))
#     plt.legend(loc='best', framealpha=.5, numpoints=1)
#     plt.xlabel('Time(s)', fontsize=14)
#     plt.ylabel('Amplitude', fontsize=14)

#     plt.show()

files = os.listdir('output')
for filename in files:
    data = pd.read_csv(os.path.join("output", filename), index=False)

    # x = [int(d[0]) for d in data]
    # y = [float(d[2]) for d in data]

    print(data)

    # df = pd.DataFrame(data, columns=['data'])
    # df['min'] = df.iloc[argrelextrema(df.data.values, lambda a,b: (a>b) | (a<b), order=10)[0]]['data']
    # df = df.dropna()
    # print(df)
    # df.to_csv(f'output1/{filename}', mode='w+', columns=['min'])