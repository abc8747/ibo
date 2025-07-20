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

# reading from the list of consituencies of hong kong
with open('boundary/boundary.json', 'r') as f:
    polygons = []
    # from all consituencies in hong kong:
    for consituency in json.load(f)["features"]:
        # select the wong tai sin district
        if consituency["properties"]["地區號碼"] == 'H':
            bounds = []
            # and since the boundary is constructed from a series of (longitude, latitude) pairs,
            # add it to the kml file
            for lon, lat in consituency["geometry"]["coordinates"][0]:
                bounds.append((lon, lat, 0))

            p = kml.Placemark()
            p.geometry = Polygon(bounds)
            d.append(p)

            break

# and export it
with open('boundary/boundary.kml', 'w+', encoding='utf-8') as fil:
    fil.write(k.to_string(prettyprint=True))