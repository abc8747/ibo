import csv

with open('LSBG_16BC.csv', 'r', encoding='utf-8-sig', newline='') as f:
    data = list(csv.reader(f))
    newdata = [data[0]]
    for d in data[1:]:
        lsbg = d[1]
        lsbgs = []

        splittedlsbgs = []

        if 'and' not in lsbg and ',' not in lsbg:
            splittedlsbgs.append(lsbg) 
        else:
            if ',' not in lsbg:
                splittedlsbgs.extend(lsbg.split(' and '))
            else:
                _1, _2 = lsbg.split(' and ')
                for _0 in _1.split(', '):
                    splittedlsbgs.append(_0)
                splittedlsbgs.append(_2)

        for l1 in splittedlsbgs:
            if '-' in l1:
                s1, s2 = l1.split('/')
                s2start, s2end = s2.split('-')
                for s3 in range(int(s2start), int(s2end) + 1):
                    lsbgs.append(f'{s1}/{str(s3).zfill(2)}')
            else:
                lsbgs.append(l1)

        for le in lsbgs:
            newdata.append([le] + d[1:])

with open('LSBG_16BC_splitted.csv', 'w+', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(newdata)