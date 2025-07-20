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

# setup kml
out = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
lineS = styles.LineStyle(width=0)
polyS = styles.PolyStyle(color='7f0000ff', outline=0)
style = styles.Style(styles=[lineS, polyS], id='all')
d = kml.Document(ns)
d.append_style(style)
out.append(d)
f = kml.Folder(ns, name='all')
d.append(f)

# setup csv
thisFolder = []

# setup input kml
with open('master.kml', 'rb') as fi:
    doc = fi.read()
inp = kml.KML()
inp.from_string(doc)

pms = list(list(inp.features())[0].features())
for pm in pms:
    if pm.styleUrl == '#icon-1899-FF5252':
        lng, lat, _ = list(pm.geometry.coords)[0]
        y, x = wgs84_to_hk80(lat, lng)
        lngMin, latMin = hk80_to_wgs84(y-200, x-200) # within a 200m square area around the POI, with tolerance 3.
        lngMax, latMax = hk80_to_wgs84(y+200, x+200)

        url = f'https://api.hkmapservice.gov.hk/ags/map/layer/ib1000//buildings/identify?key=6a40dd75bce8494ea735efd8d97dd820&f=json&tolerance=3&returnGeometry=true&imageDisplay=1000,1000,96&geometryType=esriGeometryPoint&geometry=%7B%22x%22%3A{lng},%22y%22%3A{lat}%7D&sr=4326&mapExtent={latMin},{lngMin},{latMax},{lngMax}'
        data = json.loads(http.request("GET", url).data.decode("utf-8"))['results']
        if data == []:
            print(pm.name, "failed.")
            continue
        
        baseHeight, baseSource = 0, "No data"
        roofHeight, roofSource = 0, "No data"
        polygons = []

        engBldName, chiBldName, csuid = '', '', ''

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
                if csuid == '' or 'T' in csu: # this will always guarantee that some csuid (podium/tower) will bew logged.
                    csuid = csu

            for p in r['geometry']['rings']:
                polygons.append(Polygon(p))
        
        unioned = unary_union(polygons) # UNIONs all attributes and subattributes to one polygon
        if unioned.type == 'MultiPolygon':
            unioned = unary_union(polygons[0]) # in case each building does not share the same podium, get the first one only.
        # print(url, unioned)

        # com = list(unioned.centroid.coords)[0] # get the centre of mass of the unioned polygon
        # comX, comY = wgs84_to_hk80(com[1], com[0])

        withAlt = []
        for lng, lat in list(unioned.exterior.coords):
            withAlt.append(Point(lng, lat, roofHeight)) # adds height information to the UNIONed polygon
        
        # add this building to the master folder of the KML.
        pm = kml.Placemark(ns, name=f'{pm.name}_{csuid}_{engBldName}', styleUrl='all')
        pm.geometry = kml.Geometry(geometry=Polygon(withAlt), altitude_mode='absolute', extrude=1)
        f.append(pm)

        bldgpm = kml.Placemark(ns, name=f'{pm.name}_{csuid}_{engBldName}')
        bldgpm.geometry = Point(lng, lat)
        f.append(bldgpm)

        # add this building to CSV.
        thisFolder.append((pm.name, csuid, engBldName, chiBldName, baseHeight, baseSource, roofHeight, roofSource, roofHeight-baseHeight, "x"))
        # thisFolder.append((pm.name, csuid, engBldName, chiBldName, com[0], com[1], baseHeight, baseSource, roofHeight, roofSource, roofHeight-baseHeight, "x"))

with open('3_buildings_geometry.kml', 'w', encoding='utf-8') as fil:
    fil.write(out.to_string(prettyprint=True))

with open('3_buildings_all.csv', 'w', encoding='utf-8-sig') as fil2:
    wri = csv.writer(fil2)
    wri.writerows(thisFolder)