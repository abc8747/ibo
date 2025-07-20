from pyproj import Transformer, Proj
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union
from fastkml import kml, styles
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
def getDist(x1, y1, x2, y2): return math.sqrt((x2-x1)**2+(y2-y1)**2)

allBuildings = []
k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
lineS = styles.LineStyle(width=0)
polyS = styles.PolyStyle(color='7f0000ff', outline=0)
style = styles.Style(styles=[lineS, polyS], id='all')
d = kml.Document(ns)
d.append_style(style)
k.append(d)

with open('2_buildings.kml', 'rb') as fi:
    doc = fi.read()
ko = kml.KML()
ko.from_string(doc)

for fd in list(list(ko.features())[0].features()): # for each location, make a folder.
    f = kml.Folder(ns, name=fd.name)
    d.append(f)
    thisFolder = []
    for b in list(fd.features()): # for each placemark, get their building information.
        lng, lat = list(b.geometry.coords)[0]
        y, x = wgs84_to_hk80(lat, lng)
        lngMin, latMin = hk80_to_wgs84(y-200, x-200) # within a 200m square area around the POI, with tolerance 3.
        lngMax, latMax = hk80_to_wgs84(y+200, x+200)

        url = f'https://api.hkmapservice.gov.hk/ags/map/layer/ib1000//buildings/identify?key=6a40dd75bce8494ea735efd8d97dd820&f=json&tolerance=3&returnGeometry=true&imageDisplay=1000,1000,96&geometryType=esriGeometryPoint&geometry=%7B%22x%22%3A{lng},%22y%22%3A{lat}%7D&sr=4326&mapExtent={latMin},{lngMin},{latMax},{lngMax}'
        data = json.loads(http.request("GET", url).data.decode("utf-8"))['results']
        bls, rls, polygons = [], [], []
        for r in data:
            # the building's baseLevel or roofLevel can exist in dict's lowest level or within the attribute.
            blFound = False
            if 'Base Level' in r:
                bl, blFound = float(r['Base Level']), True
            else:
                if 'attributes' in r:
                    if 'Base Level' in r['attributes']:
                        bl, blFound = float(r['attributes']['Base Level']), True
            
            if blFound: bls.append(bl)

            rlFound = False
            if 'Roof Level' in r:
                rl, rlFound = float(r['Roof Level']), True
            else:
                if 'attributes' in r:
                    if 'Roof Level' in r['attributes']:
                        rl, rlFound = float(r['attributes']['Roof Level']), True
            
            if rlFound: rls.append(rl)

            for p in r['geometry']['rings']:
                polygons.append(Polygon(p))
        
        baseHeight = min(bls) if bls != [] else 0
        roofHeight = max(rls) if rls != [] else 0
        unioned = unary_union(polygons) # UNIONs all attributes and subattributes to one polygon
        com = list(unioned.centroid.coords)[0] # get the centre of mass of the unioned polygon
        hau_dist = ()

        withAlt = []
        for lng, lat in list(unioned.exterior.coords):
            withAlt.append(Point(lng, lat, roofHeight)) # adds height information to the UNIONed polygon
        
        # add this building to KML.
        pm = kml.Placemark(ns, name=b.name, styleUrl='all')
        pm.geometry = kml.Geometry(geometry=Polygon(withAlt), altitude_mode='absolute', extrude=1)
        f.append(pm)

        # add this building to CSV.
        thisFolder.append((fd.name, b.name, com[0], com[1], baseHeight, roofHeight, roofHeight-baseHeight, "ok"))
        # format: ['1', 'ABC Building', 114.689, 22.777, 1, 20, 19]
    allBuildings.extend(thisFolder)

with open('3_buildings_geometry.kml', 'w', encoding='utf-8') as fil:
    fil.write(k.to_string(prettyprint=True))

with open('3_buildings_all.csv', 'w', encoding='utf-8-sig') as fil2:
    wri = csv.writer(fil2)
    wri.writerows(allBuildings)