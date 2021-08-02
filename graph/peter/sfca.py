import math
import csv

D_0 = 2.16*1000

def f(D_ij, D_0):
    if D_ij < D_0:
        return (math.exp(-0.5*(math.pow((D_ij/D_0), 2))) - math.exp(-0.5)) / (1-math.exp(-0.5))
    else:
        return 0

def loadData():
    with open('data.csv', 'r+', newline='', encoding='utf-8-sig') as f:
        data = list(csv.reader(f))
        print(data)

loadData()

    # return val