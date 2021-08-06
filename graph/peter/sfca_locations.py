import csv
from commons import common
from rich import print, inspect
from rich.progress import track

with open(f'sample/sample.csv', 'r', encoding='utf-8-sig', newline='') as f:
    data = list(csv.reader(f))[1:]
    samples = [common.Sample(d[0], d[1], d[2]) for d in data]

with open(f'population/population.csv', 'r', encoding='utf-8-sig', newline='') as f:
    data = list(csv.reader(f))[1:]
    buildings = [common.Building(d[0], d[1], d[2], d[3], d[4]) for d in data]

for cat, catchment_distance in [(1, 666), (2, 1000), (3, 666)]:
    with open(f'cat{cat}/cat{cat}.csv', 'r', encoding='utf-8-sig', newline='') as f:
        data = list(csv.reader(f))[1:]
        locations = [common.Location(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]) for d in data]
        
        samples = []
        for d in data:
            coords = common.Coordinate(lat=d[5], lon=d[6])
            samples.append(common.Sample(d[0], coords.x, coords.y))

        print(samples)
        # break

        # perform SFCA
        newdata = [common.Sample.csvheaders]
        sfca = common.SFCA(samples=samples, locations=locations, buildings=buildings, catchment_distance=catchment_distance).calculate()
        for sample in sfca.samples:
            newdata.append(sample.genRow())
        
    with open(f'cat{cat}/sample{cat}_locations.csv', 'w+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(newdata)