import csv
import urllib
import urllib3
import json

http = urllib3.PoolManager()

with open('data.csv', 'r+', encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))
    for r in rows:
        geoAddr = r[1]
        bldName = r[2]
        if geoAddr:
            hasErr = False
            d = json.loads(http.request('GET', f'https://www.als.ogcio.gov.hk/galookup?{urllib.parse.urlencode({"ga":geoAddr})}', headers={
                'Accept': 'application/json'
            }).data.decode('utf-8'))

            if 'SuggestedAddress' not in d:
                hasErr = True
                d = json.loads(http.request('GET', f'https://www.als.ogcio.gov.hk/lookup?{urllib.parse.urlencode({"q":bldName})}', headers={
                    'Accept': 'application/json'
                }).data.decode('utf-8'))

            # print(json.dumps(d, indent=4, ensure_ascii=False))
            if 'SuggestedAddress' in d:
                eng = d['SuggestedAddress'][0]['Address']['PremisesAddress']['EngPremisesAddress']
                try:
                    stFrom = eng['EngStreet']['BuildingNoFrom']
                except:
                    stFrom = "?"

                try:
                    stTo = f"-{eng['EngStreet']['BuildingNoTo']}"
                except:
                    stTo = ""
                st = eng['EngStreet']['StreetName']
                district = eng['EngDistrict']['DcDistrict']

                addr = f'{stFrom}{stTo} {st}'
                errIndicator = "*" if hasErr else ""

                r.extend((addr, errIndicator))
                print(r[0])


with open('dataMore.csv', 'w+', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerows(rows)