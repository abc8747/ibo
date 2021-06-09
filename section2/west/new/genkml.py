from pyproj import Transformer, Proj
from shapely.geometry import Point, LineString
from fastkml import kml
import math
import urllib3
import json
import itertools
import csv

http = urllib3.PoolManager()
hk80_to_wgs84 = Transformer.from_crs("epsg:2326", "epsg:4326").transform
wgs84_to_hk80 = Transformer.from_crs("epsg:4326", "epsg:2326").transform
hk80 = Proj('epsg:2326')
wgs84 = Proj('epsg:4326')


allBuildings = []
k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
d = kml.Document(ns)
k.append(d)


with open('1_out.csv', 'r', encoding='utf-8-sig') as fi:
    old = list(csv.reader(fi))
    folders = {}
    for row in old:
        foldername = row[0][1:][:-2]
        if foldername not in folders:
            folders[foldername] = []
        folders[foldername].append(row)
    # print(folders)

for foldername in folders.keys():
    f = kml.Folder(ns, name=foldername)
    for detail in folders[foldername]:
        if len(detail) <= 3:
            print(detail[0])
            continue
        print(f'{detail[0]} - {detail[3]}')
        x, y = detail[-2:]
        # url = f'https://api.hkmapservice.gov.hk/ags/gc/loc/buildingcsuid/reverseGeocode?key=584b2fa686f14ba283874318b3b8d6b0&outSR=%7B%22wkid%22:2326%7D&location=%7B%22x%22:{x},%22y%22:{y},%22spatialReference%22:%7B%22wkid%22:2326,%22latestWkid%22:2326%7D%7D&distance=100&f=json'
        # data = json.loads(http.request("GET", url).data.decode("utf-8"))
        # if "error" in data:
        #     print(f'!!    {url}')
        #     print(f'!!    {data}')
        #     continue
        # print(f'      {data["location"]}')
        try:
            lat, lng = hk80_to_wgs84(x, y)
            p = kml.Placemark(ns, name=f'{detail[0]} - {detail[3]}')
            p.geometry = Point(lng, lat)
            f.append(p)
        except:
            pass
    d.append(f)

with open('2_buildings.kml', 'w', encoding='utf-8') as fil:
    fil.write(k.to_string(prettyprint=True))