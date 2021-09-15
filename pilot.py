'''
This script does the following:
- calculate T for 0.001 < l < 1.500, with increments of 0.001
- save the raw data to a CSV file.
- for 0.001 < l < 1.500, with increments of 0.001:
    - for 0.0010 < r < 0.0979, with increments of 0.0001:
        - calculate the percentage error in T
        - plot on a 2D axis with the 'turbo' colormap
- store the graph in a PNG image.
'''

import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

g = 9.81

def getT(l_rod, r, l):
    return 2*math.pi*l_rod/r*math.sqrt(l/12/g)

def getTerr(l_rod, 𝛿l_rod, r, 𝛿r, l, 𝛿l):
    return math.sqrt(
        math.pow((𝛿l_rod*math.pi*math.sqrt(l/g)) / (math.sqrt(3)*r), 2) +
        math.pow((𝛿r*math.pi*l_rod*math.sqrt(l/g)) / (math.sqrt(3)*math.pow(r, 2)), 2) +
        math.pow((𝛿l*math.pi*l_rod*math.sqrt(l/g)) / (math.sqrt(3)*r*l*2), 2)
    )

df0 = pd.DataFrame([(l, getT(.1958, .075, l)) for l in np.arange(.001, 1.500, .001)], columns=['l', 'T'])
df0.to_csv('output1/pilot.csv', index=False)

data = []
l_rod, 𝛿l_rod = .1958, .0001
𝛿l = .001
𝛿r = .001
for l in np.arange(.001, 1.500, .001):
    for r in np.arange(.001, .0979, .0001):
        pct𝛿T = min(getTerr(l_rod, 𝛿l_rod, r, 𝛿r, l, 𝛿l) / getT(l_rod, r, l), .025)
        data.append([l, r, pct𝛿T])

df = pd.DataFrame(data, columns=['l', 'r', 'pct𝛿T'])
plt.rcParams['font.family'] = 'Latin Modern Roman'
plt.scatter(x=df['l'],y=df['r'],c=df['pct𝛿T'], cmap='turbo')
plt.xlim([.001, 1.500])
plt.ylim([.001, .0979])
plt.savefig('output1/pilot.png', dpi=300)