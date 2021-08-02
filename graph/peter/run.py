import csv
# import sys
# sys.path.append(".")
from commons import common

cat = 3

# get missing addresses
with open(f'cat{cat}/raw.csv', 'r', encoding='utf-8-sig', newline='') as f:
    data = list(csv.reader(f))
    for r in data[1:]:
        if r[2] == '':
            location = common.Location()
            location.getLocations(r[1]).setLocation()
            break