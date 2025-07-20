import os
import json
import matplotlib.pyplot as plt

jsons = os.listdir('./data/')

buildings = []
for j in jsons:
    with open(f'data/{j}', mode='r+', encoding='utf-8') as f:
        buildings.extend(json.load(f))

x = []
y1 = []
y1a = []
y2 = []

for b in buildings:
    try:
        if float(b['roofHeight']) > 0 and float(b['baseHeight']) > 0 and b['gross'] > 0:
            rh = float(b['roofHeight'])
            bh = float(b['baseHeight'])
            g = float(b['gross'])
            lng, lat = b['geometry'][0]

            x.append(lat)
            y1.append(rh-bh)
            y1a.append(bh)
            y2.append(g)
    except:
        pass

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.errorbar(x, y1, yerr=[y1, [0 for k in range(len(y1))]], ls="None")
ax1.set_xlim(22.26,22.43)
ax1.set_ylim(0, 250)

# ax1.errorbar(x, y1a, yerr=[[0 for k in range(len(y1))], y1], ls="None")
# ax1.set_xlim(22.26,22.43)
# ax1.set_ylim(0, 500)

ax2.plot(x, y2, marker='x', color='black',linestyle="None")
ax2.set_xlim(22.26,22.43)
ax2.set_ylim(0, 60000)

plt.show()
