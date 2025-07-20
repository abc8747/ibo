import csv
import urllib
import urllib3
import json

http = urllib3.PoolManager()

with open('original.csv', 'r+', encoding='utf-8-sig') as f:
    old = list(csv.reader(f))
    for r in old:
        if len(r) == 1:
            r.append('')
            r.append('')
        if len(r) == 2:
            r.append('')
        if len(r) > 3:
            continue

        print(f'===== {r[0]} =====')
        for c in r[1:]:
            try:
                d = json.loads(http.request('GET', f'https://www.als.ogcio.gov.hk/lookup?{urllib.parse.urlencode({"q":c})}', headers={
                    'Accept': 'application/json'
                }).data.decode('utf-8'))

                try:
                    bn = d['SuggestedAddress'][0]['Address']['PremisesAddress']['EngPremisesAddress']['BuildingName']
                except:
                    bn = '?'
                cs = d['SuggestedAddress'][0]['Address']['PremisesAddress']['GeoAddress']
                n = d['SuggestedAddress'][0]['Address']['PremisesAddress']['GeospatialInformation']['Northing']
                e = d['SuggestedAddress'][0]['Address']['PremisesAddress']['GeospatialInformation']['Easting']
                if bn:
                    r.extend((bn, cs, n, e))
                    break
            except:
                pass
        print(r)

with open('1_out.csv', 'w+') as f:
    w = csv.writer(f)
    w.writerows(old)
            # print(r[0], url, x)