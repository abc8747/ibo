import os
import json
import matplotlib.cm
jsons = os.listdir('./data/')
cmap = matplotlib.cm.get_cmap('hot')

colors = []
for i in range(101):
    c = cmap(i, bytes=True)
    colors.append(f'ff{hex(c[2])[2:].zfill(2)}{hex(c[1])[2:].zfill(2)}{hex(c[0])[2:].zfill(2)}')
colorDefinitions = ""
for c in colors:
    colorDefinitions += f"""
<Style id="{c}">
    <LineStyle>
        <width>0</width>
    </LineStyle>
    <PolyStyle>
        <color>{c}</color>
        <outline>0</outline>
    </PolyStyle>
</Style>"""

buildings = []
for j in jsons:
    with open(f'data/{j}', mode='r+', encoding='utf-8') as f:
        buildings.extend(json.load(f))

# for j in jsons[:1]:
#     places = ''
#     with open(f'data/{j}', mode='r+', encoding='utf-8') as f:
#         buildings = json.load(f)
if 1:
    if 1:       
        places = '' 
        a = []
        for b in buildings:
            try:
                if float(b['roofHeight']) > 0 and float(b['baseHeight']) > 0:
                    a.append(float(b['roofHeight']) - float(b['baseHeight']))
            except:
                pass

        mx = max(a)
        mn = min(a)
        def getColor(this, mn, mx):
            return colors[100-int(100*(this-mn)/(mx-mn))]
        addedTypeCodes = []
        for b in buildings:
            try:
                if b['typeCode'] not in addedTypeCodes and b['effective'] > 0 and float(b['roofHeight']) > 0 and float(b['baseHeight']) > 0 and b['geometry'] != []:
                    coordstring = ''
                    for c in b['geometry']:
                        coordstring += f"{c[0]},{c[1]},{b['effective']*0.01} "
                    # if float(b['roofHeight']) - float(b['baseHeight']) == mx:
                    #     print(b['typeCode'])
                    
                    thisPlace = f"""        <Placemark>
        <name>{b['typeCode']}</name>
        <styleUrl>#{getColor(float(b['roofHeight'])-float(b['baseHeight']), mn, mx)}</styleUrl>
        <Polygon>
            <extrude>1</extrude>
            <altitudeMode>relativeToSeaFloor</altitudeMode>
            <outerBoundaryIs>
                <LinearRing>
                    <coordinates>
                        {coordstring[:-1]}
                    </coordinates>
                </LinearRing>
            </outerBoundaryIs>
        </Polygon>
    </Placemark>"""
                    places += thisPlace
                    addedTypeCodes.append(b['typeCode'])
            except:
                pass

    doc = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <name>polygontest.kml</name>
{colorDefinitions}
{places}
</Document>
</kml>'''
    print(doc)