import csv
from commons import common
from rich import print, inspect
from rich.progress import track



# query placeids, lat, lng and address info using Geocoding API.
for cat in [1,2,3]:
    with open(f'cat{cat}/cat{cat}.csv', 'r', encoding='utf-8-sig', newline='') as f:
        data = list(csv.reader(f))[1:]
        routes = common.Routes(data).getRoutes().routes

    with open(f'cat{cat}/routes_walking{cat}.csv', 'w+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(routes)