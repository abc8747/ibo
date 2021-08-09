from rich import print, inspect
import csv
from db import common

with open(f'out/survey.csv', 'r+', encoding='utf-8-sig', newline='') as f:
    data = list(csv.reader(f))
    data[0].append('code')
    newdata = [data[0]]

    for d in data[1:]:
        coords = common.Coordinate(x=d[1], y=d[2])
        coords.geocode()
        d.append(f'{coords.code}')
        # d.append(coords.code)
        newdata.append(d)

with open(f'out/survey_new.csv', 'w+', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(newdata)