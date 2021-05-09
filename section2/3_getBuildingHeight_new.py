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
f = kml.Folder(ns, name='all')
d.append(f)

with open('2_buildings.kml', 'rb') as fi:
    doc = fi.read()
ko = kml.KML()
ko.from_string(doc)

with open('1_separated.kml', 'rb') as fi_1:
    doc = fi_1.read()
raw1 = kml.KML()
raw1.from_string(doc)
ptCoords = list(list(list(list(raw1.features())[0].features())[0].features())[0].geometry.coords)

for counter, coordinate in enumerate(ptCoords):
    ln, lt = coordinate
    tspm = kml.Placemark(ns, name=str(counter))
    tspm.geometry = Point(ln, lt)

with open('0_raw.kml', 'rb') as fi_0:
    docR = fi_0.read()
raw0 = kml.KML()
raw0.from_string(docR)
coords = list(list(list(list(raw0.features())[0].features())[0].features())[0].geometry.coords)

pts = []
for coordinate in coords:
    ln, lt = coordinate
    x, y = wgs84_to_hk80(lt, ln)
    pts.append(Point(x, y))
rawLine = LineString(pts)

thisFolder = []
pm_list = []
bldgpm_list = []

for counter, fd in enumerate(list(list(ko.features())[0].features())): # for each location, make a folder.
    for b in list(fd.features()): # for each placemark, get their building information.
        lng, lat, _ = list(b.geometry.coords)[0]
        y, x = wgs84_to_hk80(lat, lng)
        lngMin, latMin = hk80_to_wgs84(y-200, x-200) # within a 200m square area around the POI, with tolerance 3.
        lngMax, latMax = hk80_to_wgs84(y+200, x+200)

        url = f'https://api.hkmapservice.gov.hk/ags/map/layer/ib1000//buildings/identify?key=6a40dd75bce8494ea735efd8d97dd820&f=json&tolerance=3&returnGeometry=true&imageDisplay=1000,1000,96&geometryType=esriGeometryPoint&geometry=%7B%22x%22%3A{lng},%22y%22%3A{lat}%7D&sr=4326&mapExtent={latMin},{lngMin},{latMax},{lngMax}'
        data = json.loads(http.request("GET", url).data.decode("utf-8"))['results']
        if data == []:
            print(f'{counter} failed at ({lng}, {lat}) / {b.name}.')
            continue
        
        baseHeight, baseSource = 0, "No data"
        roofHeight, roofSource = 0, "No data"
        polygons = []

        engBldName, chiBldName, csuid, buildingid = '', '', '', ''

        for r in data:
            # the building's baseLevel or roofLevel can exist in dict's lowest level or within the attribute.
            try:
                bh, bhs = float(r['Base Level']), r['Base Level Data Source']
            except:
                try:
                    bh, bhs = float(r['attributes']['Base Level']), r['attributes']['Base Level Data Source']
                except:
                    bh, bhs = -1, 'Error'
            finally:
                if bh > baseHeight:
                    baseHeight, baseSource = bh, bhs

            try:
                rh, rhs = float(r['Roof Level']), r['Roof Level Data Source']
            except:
                try:
                    rh, rhs = float(r['attributes']['Roof Level']), r['attributes']['Roof Level Data Source']
                except:
                    rh, rhs = -1, 'Error'
            finally:
                if rh > roofHeight:
                    roofHeight, roofSource = rh, rhs
            
            # get the building's relevant english and chinese building name and csuid.
            try:
                en = r['English Building Name']
            except:
                try:
                    en = r['attributes']['English Building Name']
                except:
                    en = ''
            finally:
                if en != "Null" and len(en) > len(engBldName):
                    engBldName = en

            try:
                ch = r['Chinese Building Name']
            except:
                try:
                    ch = r['attributes']['Chinese Building Name']
                except:
                    ch = ''
            finally:
                if ch != "Null" and len(ch) > len(chiBldName):
                    chiBldName = ch

            try:
                csu = r['buildingcsuid']
            except:
                try:
                    csu = r['attributes']['buildingcsuid']
                except:
                    csu = ''
            finally:
                if csuid == '' or 'T' in csu: # this will always guarantee that some csuid (podium/tower) will be logged.
                    csuid = csu
                    buildingid = r['attributes']['Building ID']

        for r in data:
            try:
                rh = float(r['Roof Level'])
            except:
                try:
                    rh = float(r['attributes']['Roof Level'])
                except:
                    rh = -1
            finally:
                if rh == roofHeight:
                    for p in r['geometry']['rings']:
                        polygons.append(Polygon(p))
        
        unioned = unary_union(polygons) # UNIONs all attributes and subattributes to one polygon
        if unioned.type == 'MultiPolygon':
            unioned = unary_union(polygons[0]) # in case each building does not share the same podium, get the first one only.

        # print(unioned.centroid)
        comlng, comlat = unioned.centroid.x, unioned.centroid.y
        comX, comY = wgs84_to_hk80(comlat, comlng)
        # print(comlng, comlat, comX, comY)

        # comX, comY = int(f'8{csuid[:5]}'), int(f'8{csuid[5:10]}')
        # comlat, comlng = hk80_to_wgs84(comY, comX)
        # print(comlng, comlat)
        pro = rawLine.project(Point(comX, comY))

        withAlt = []
        for lng, lat in list(unioned.exterior.coords):
            withAlt.append(Point(lng, lat, roofHeight)) # adds height information to the UNIONed polygon
        
        # add this building to the master folder of the KML.
        pm = kml.Placemark(ns, name=f'{counter}_{engBldName}', styleUrl='all')
        pm.geometry = kml.Geometry(geometry=Polygon(withAlt), altitude_mode='absolute', extrude=1)
        pm_list.append(pm)

        bldgpm = kml.Placemark(ns, name=f'{counter}_{engBldName}')
        bldgpm.geometry = Point(comlng, comlat)
        bldgpm_list.append(bldgpm)
        # add this building to CSV.
        thisFolder.append((counter, csuid, buildingid, engBldName, chiBldName, comlng, comlat, pro, baseHeight, baseSource, roofHeight, roofSource, roofHeight-baseHeight, "x"))

for pm in pm_list:
    f.append(pm)

for bldgpm in bldgpm_list:
    f.append(bldgpm)

with open('3_buildings_geometry.kml', 'w', encoding='utf-8') as fil:
    fil.write(k.to_string(prettyprint=True))

with open('3_buildings_all.csv', 'w', encoding='utf-8-sig') as fil2:
    wri = csv.writer(fil2)
    wri.writerows(thisFolder)