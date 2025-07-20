import csv
import requests
import re

def findBetween(s, start, end):
    return s[s.find(start)+len(start):s.rfind(end)]

with open('analysed.csv', 'r+', encoding='utf-8-sig', newline='') as f:
    data = list(csv.reader(f))
    counter = 1000
    for d in data[counter:]:
        url = f"http://hk.centamap.com/gprop1/iprop.aspx?ck=gprop1&lg=&cx=&cy=&zm=0&itemid={d[0][2:]}&ft0=&ft1=&ft2="
        r = requests.request("GET", url).text
        if "error" in r:
            print(f"{counter},{d[0]},")
        else:
            floors = findBetween(r, 'No. of Floor: ', ' floor')
            print(f"{counter},{d[0]},{floors}")
        counter += 1

    # for d in data:
    #     print(d[0])