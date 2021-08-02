import csv
from commons import common
from rich import print, inspect
from rich.progress import track
import os

# query placeids, lat, lng and address info using Geocoding API.
for cat in [1, 2, 3]:
    with open(f'cat{cat}/cat{cat}.csv', 'r', encoding='utf-8-sig', newline='') as f:
        data = list(csv.reader(f))
        newdata = [common.Location.csvheaders]
        for r in data[1:]:
            newdata.append(common.Location(locationid=r[0], name=r[1], query=r[2], number=r[3]).geocode().genRow())

    os.rename(f'cat{cat}/cat{cat}.csv', f'cat{cat}/cat{cat}.csv.old')

    with open(f'cat{cat}/cat{cat}.csv', 'w+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(newdata)