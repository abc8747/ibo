import json
from fastkml import kml
from shapely.geometry import Polygon

k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
d = kml.Document(ns, 'docid', 'doc name', 'doc description')
k.append(d)
f = kml.Folder(ns, 'fid', 'f name', 'f description')

with open('DCCA2019.json', 'r') as f:
    for consituency in json.load(f):
        if 'H' in consituency['CACODE']:
            geo = consituency['json_geometry']['coordinates'][0]
            p = kml.Placemark(ns, consituency['CACODE'], consituency['ENAME'], 'description')
            print(geo)