import csv
from commons import common
from rich import print, inspect
from rich.progress import track

# loc = common.Location('0', 'TEST', 'Winning Centre, 29 Tai Yau Street, San Po Kong, Kowloon', '49').geocode()
# inspect(loc)

# query placeids, lat, lng and address info using Geocoding API.
for cat in [3]:
    with open(f'cat{cat}/raw{cat}.csv', 'r', encoding='utf-8-sig', newline='') as f:
        data = list(csv.reader(f))[1:]
        newdata = [common.Location.csvheaders]
        for r in data:
            newdata.append(common.Location(locationid=r[0], name=r[1], query=r[2], number=r[3]).geocode().genRow())

    with open(f'cat{cat}/cat{cat}.csv', 'w+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(newdata)