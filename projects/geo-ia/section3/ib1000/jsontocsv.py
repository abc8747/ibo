import json
import csv

with open('out.json', 'r+') as infile:
    x = json.load(infile)

c = []
for k in x.keys():
    if x[k]:
        r = k.split('_')
        r.extend(list(x[k][0].values()))
        c.append(r)
# print(c)

with open('out.csv', 'w+') as outfile:
    wri = csv.writer(outfile)
    wri.writerows(c)