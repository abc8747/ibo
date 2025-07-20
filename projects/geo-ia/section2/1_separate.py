from pyproj import Transformer, Proj
from shapely.geometry import Point, LineString
from fastkml import kml
import math

hk80_to_wgs84 = Transformer.from_crs("epsg:2326", "epsg:4326").transform
wgs84_to_hk80 = Transformer.from_crs("epsg:4326", "epsg:2326").transform
hk80 = Proj('epsg:2326')
wgs84 = Proj('epsg:4326')
def getDist(x1, y1, x2, y2): return math.sqrt((x2-x1)**2+(y2-y1)**2)

pts = []
pts_interpolated = []

with open('0_raw.kml', 'rb') as f:
    doc = f.read()
ko = kml.KML()
ko.from_string(doc)
coords = list(list(list(list(ko.features())[0].features())[0].features())[0].geometry.coords)

for coordinate in coords:
    ln, lt = coordinate
    x, y = wgs84_to_hk80(lt, ln)
    pts.append(Point(x, y))

ptsDist = sum([getDist(pts[p+1].x, pts[p+1].y, pts[p].x, pts[p].y) for p in range(len(pts)-1)])
# ptsDist = sum([math.sqrt((pts[p+1].x - pts[p].x)**2 + (pts[p+1].y - pts[p].y)**2) for p in range(len(pts)-1)])
line = LineString(pts)
for distanceToOrigin in range(0, math.ceil(ptsDist)+1, 200):
    loc = line.interpolate(distanceToOrigin)
    lt, ln = hk80_to_wgs84(loc.x, loc.y)
    pts_interpolated.append(Point(ln, lt))

k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
d = kml.Document(ns)
k.append(d)
f = kml.Folder(ns)
d.append(f)

l = kml.Placemark(ns)
l.geometry = LineString(pts_interpolated)
f.append(l)
for p_interp in pts_interpolated:
    l1 = kml.Placemark(ns)
    l1.geometry = p_interp
    f.append(l1)

with open('1_separated.kml', 'w', encoding='utf-8') as f:
    f.write(k.to_string(prettyprint=True))