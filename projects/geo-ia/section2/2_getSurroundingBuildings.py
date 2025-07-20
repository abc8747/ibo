from pyproj import Transformer, Proj
from shapely.geometry import Point, LineString
from fastkml import kml
import math
import urllib3
import json
import itertools

http = urllib3.PoolManager()
hk80_to_wgs84 = Transformer.from_crs("epsg:2326", "epsg:4326").transform
wgs84_to_hk80 = Transformer.from_crs("epsg:4326", "epsg:2326").transform
hk80 = Proj('epsg:2326')
wgs84 = Proj('epsg:4326')
probeDistances = (15, 20, 25, 30)
degreeIncrements = 10

def toRad(deg): return deg*math.pi/180
def getDist(x1, y1, x2, y2): return math.sqrt((x2-x1)**2+(y2-y1)**2)
def getProbes(dist): return [(dist*math.sin(toRad(a)), dist*math.cos(toRad(a))) for a in range(0, 360, degreeIncrements)]

allBuildings = []
probeOffsets = []
for pd in probeDistances:
    probeOffsets.extend([o for o in getProbes(pd)])
k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
d = kml.Document(ns)
k.append(d)


with open('1_separated.kml', 'rb') as fi:
    doc = fi.read()
ko = kml.KML()
ko.from_string(doc)
coords = list(list(list(list(ko.features())[0].features())[0].features())[0].geometry.coords)
for counter, coordinate in enumerate(coords):
    # create a folder to store the placemarks
    f = kml.Folder(ns, name=str(counter))
    d.append(f)

    buildings = []
    ln, lt = coordinate
    y, x = wgs84_to_hk80(lt, ln)
    # probe for buildings in the 20m and 40m vicinity, at 0, 45, 90, 135, 180, 225, 270, 325 degrees.
    for po in probeOffsets:
        data = json.loads(http.request("GET", f'https://api.hkmapservice.gov.hk/ags/gc/loc/buildingcsuid/reverseGeocode?key=584b2fa686f14ba283874318b3b8d6b0&outSR=%7B%22wkid%22:2326%7D&location=%7B%22x%22:{x+po[0]},%22y%22:{y+po[1]},%22spatialReference%22:%7B%22wkid%22:2326,%22latestWkid%22:2326%7D%7D&distance=100&f=json').data.decode("utf-8"))
        if "error" in data:
            continue
        currAddress = data['address']['Address']
        if currAddress not in buildings:
            lat, lng = hk80_to_wgs84(data['location']['y'], data['location']['x'])
            p = kml.Placemark(ns, name=currAddress)
            p.geometry = Point(lng, lat)
            f.append(p)
            buildings.append(currAddress)
            print(f'--> {currAddress}')

    print(f'{counter} @ {coordinate} done.')

with open('2_buildings.kml', 'w', encoding='utf-8') as fil:
    fil.write(k.to_string(prettyprint=True))