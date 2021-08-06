import csv
from commons import common
from rich import print, inspect
from rich.progress import track

newdata = []

for cat in [1,2,3]:
    with open(f'cat{cat}/sample{cat}_locations.csv', 'r', encoding='utf-8-sig', newline='') as f:
        data = list(csv.reader(f))[1:]
        thismaxaccessibility = max(map(lambda d:float(d[3]), data))
        for d in data:
            s = common.Sample(d[0], d[1], d[2], float(d[3])/thismaxaccessibility)
            for newd in newdata:
                if newd.sampleid == s.sampleid:
                    newd.accessibility += s.accessibility
                    # print(newd.sampleid, newd.accessibility)
                    break
            else:
                newdata.append(s)
                # print(s.sampleid, s.accessibility)

with open(f'catall/sampleall_locations.csv', 'w+', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([common.Sample.csvheaders] + [d.genRow() for d in newdata])

# inspect(newdata)