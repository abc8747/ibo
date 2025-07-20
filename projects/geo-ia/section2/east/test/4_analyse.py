import csv

def getAvg(l): return sum(l)/len(l)
def getUnc(l): return (max(l)-min(l))/2

d1 = []

with open('3_buildings_all.csv', 'r+', encoding='utf-8-sig') as f:
    data = list(csv.reader(f))
    keys = list(set((k[0] for k in data)))
    for key in keys:
        ok = []
        full = []
        for d in data:
            if d[0] == key:
                if d[-1] == 'ok':
                    ok.append(float(d[-2]))
                full.append(float(d[-2]))
        d1.append([key, getAvg(ok), getUnc(ok), getAvg(full), getUnc(full)])

with open('4_analysed.csv', 'w', encoding='utf-8-sig') as g:
    wri = csv.writer(g)
    wri.writerows(d1)