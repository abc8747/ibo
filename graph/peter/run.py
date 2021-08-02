import csv
from commons import common
from rich import print, inspect
from rich.progress import track

# get missing addresses
for cat in [1]:
    newdata = []
    with open(f'cat{cat}/raw.csv', 'r', encoding='utf-8-sig', newline='') as f:
        data = list(csv.reader(f))
        data[0].extend(("lat", "lon"))
        newdata = [data[0]]
        for r in data[1:]:
            try:
                if r[2] == '':
                    # address is missing, so search by name
                    location = common.Location(locationid=r[0], description=r[1], number=r[3])
                    location.geocode(r[1])
                    # location.getLocations(r[1]).setLocation()
                else:
                    # _addr = ", ".join(r[2].split(", ")[-4:])
                    location = common.Location(locationid=r[0], description=r[1], address=r[2], number=r[3])
                    location.geocode(r[2])
                    # location.getLocations(r[2]).setLocation()
                inspect(location, private=False)
                newdata.append([location.locationid, location.description, location.address, location.number, location.lat, location.lon])
            except:
                r.extend(['', ''])
                newdata.append(r)
            break

    print(newdata)

    with open(f'cat{cat}/raw1.csv', 'w+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(newdata)