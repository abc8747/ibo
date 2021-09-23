import csv
from commons import common
from rich import print, inspect
from rich.progress import track

for cat in [3]:
    with open(f'cat{cat}/raw{cat}.csv', 'r', encoding='utf-8-sig', newline='') as f:
        data = list(csv.reader(f))[1:]
        newdata = [common.Location.csvheaders]
        # converts raw WGS84 lat/lon pairs to HK80 x/y coordinates
        # by passing through an internal Location() class
        for r in data:
            newdata.append(common.Location(locationid=r[0], name=r[1], query=r[2], number=r[3]).geocode().genRow())

    # export 
    with open(f'cat{cat}/cat{cat}.csv', 'w+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(newdata)