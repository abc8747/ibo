from fastkml import kml, styles

with open('buildingMarkers.kml', 'rb') as f:
    doc = f.read()
kold = kml.KML()
kold.from_string(doc)

k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
iconS = styles.IconStyle(icon_href='https://drive.google.com/uc?export=download&id=1SFOawBgCpKkqOV1Tf96A6Khhl4HKgU2G', scale=0.01)

# lineS = styles.LineStyle(width=0)
# polyS = styles.PolyStyle(color='7f0000ff', outline=0)
style = styles.Style(styles=[iconS], id='universal')
d = kml.Document(ns)
d.append_style(style)
k.append(d)


for folder in list(list(kold.features())[0].features()):
    f = kml.Folder(ns)
    d.append(f)
    for placemark in list(folder.features()):
        placemark.styleUrl = 'universal'
        d.append(placemark)
        print(placemark.styleUrl)
    print('--')

with open('buildingMarkers_n.kml', 'w', encoding='utf-8') as fil:
    fil.write(k.to_string(prettyprint=True))