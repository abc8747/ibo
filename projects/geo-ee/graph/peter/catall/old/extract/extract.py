from pyproj import Transformer, Proj
from shapely.geometry import Point, LineString
from fastkml import kml
import csv


with open('doc.kml', 'rb') as fi:
    doc = fi.read()
ko = kml.KML()
ko.from_string(doc)
det = []
for folder in list(list(ko.features())[0].features()):
    foldername = folder.name
    print(f'>>> {foldername}')
    for placemark in list(folder.features()):
        det.append([
            placemark.name,
            placemark.geometry.y,
            placemark.geometry.x,
            foldername
        ])

with open('data.csv', 'w+', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(det)