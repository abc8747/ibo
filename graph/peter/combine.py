import csv
from commons import common

isSample = True # configuration for whether to analyse samples or individual locations
newdata = []

# for each category 1, 2, 3
for cat in [1,2,3]:
    with open(f'cat{cat}/sample{cat}.csv' if isSample else f'cat{cat}/sample{cat}_locations.csv', 'r', encoding='utf-8-sig', newline='') as f:
        data = list(csv.reader(f))[1:]
        thismaxaccessibility = max(map(lambda d:float(d[3]), data))
        # for each sample in this category,
        for d in data:
            s = common.Sample(d[0], d[1], d[2], float(d[3])/thismaxaccessibility)
            for newd in newdata:
                if newd.sampleid == s.sampleid:
                    # sum up the accessibility.
                    newd.accessibility += s.accessibility
                    break
            else:
                newdata.append(s)

# output the summed accessibilities
with open(f'catall/sampleall.csv' if isSample else f'catall/sampleall_locations.csv', 'w+', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([common.Sample.csvheaders] + [d.genRow() for d in newdata])