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

with open('boundary/boundary.json', 'r') as f:
    polygons = []
    for consituency in json.load(f)["features"]:
        if consituency["properties"]["地區號碼"] == 'H':
            bounds = []
            for lon, lat in consituency["geometry"]["coordinates"][0]:
                bounds.append((lon, lat, 0))

            p = kml.Placemark()
            p.geometry = Polygon(bounds)
            d.append(p)

            break

with open('boundary/boundary.kml', 'w+', encoding='utf-8') as fil:
    fil.write(k.to_string(prettyprint=True))