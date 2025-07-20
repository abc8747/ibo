import json
from fastkml import kml
from rich import inspect, print
from shapely.geometry import Polygon
from shapely.ops import unary_union
from commons import common

k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
d = kml.Document(ns)
k.append(d)

# with open('boundary/DCCA2019.json', 'r') as f:
#     for consituency in json.load(f):
#         if 'H' in consituency['CACODE']:
#             bounds = []
#             for y, x in consituency['json_geometry']['coordinates'][0]:
#                 coords = common.Coordinate(x=x, y=y)
#                 bounds.append((coords.lon, coords.lat, 0))

#             p = kml.Placemark(ns, id=consituency['CACODE'], name=consituency['ENAME'])
#             p.geometry = Polygon(bounds)
#             d.append(p)
            # inspect(bounds)

with open('boundary/DCCA2019.json', 'r') as f:
    polygons = []
    for consituency in json.load(f):
        if 'H' in consituency['CACODE']:
            polygons.append(Polygon(consituency['json_geometry']['coordinates'][0]))

    bounds = []
    for y, x in unary_union(polygons).exterior.coords:
        coords = common.Coordinate(x=x, y=y)
        bounds.append((coords.lon, coords.lat, 0))

    p = kml.Placemark()
    p.geometry = Polygon(bounds)
    d.append(p)

with open('boundary/boundary.kml', 'w+', encoding='utf-8') as fil:
    fil.write(k.to_string(prettyprint=True))