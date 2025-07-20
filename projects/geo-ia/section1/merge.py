import os
import json

files = os.listdir('data')

alldata = []

for fi in files:
    with open(f"data/{fi}", "r", encoding='utf-8') as f:
        d = json.load(f)
        for i in d['data']:
            alldata.append(i)

with open(f"merged.json", "w+", encoding='utf-8') as g:
    json.dump({"data": alldata}, g, ensure_ascii=False)