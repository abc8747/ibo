import json
from fastkml import kml
from rich import inspect, print
from shapely.geometry import Polygon
from commons import common

k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
d = kml.Document(ns)
k.append(d)

with open('boundary/DCCA2019.json', 'r') as f:
    for consituency in json.load(f):
        if 'H' in consituency['CACODE']:
            bounds = []
            for y, x in consituency['json_geometry']['coordinates'][0]:
                coords = common.Coordinate(x=x, y=y)
                bounds.append((coords.lon, coords.lat, 0)) # google reverses this

            p = kml.Placemark(ns, id=consituency['CACODE'], name=consituency['ENAME'])
            p.geometry = Polygon(bounds)
            d.append(p)
            # inspect(bounds)

with open('boundary/boundary.kml', 'w+', encoding='utf-8') as fil:
    print(k.to_string(prettyprint=True))
    fil.write(k.to_string(prettyprint=True))