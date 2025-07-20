import json
import csv

master = []

def getValue(dictionary, name):
    return dictionary[name] if name in dictionary else ''

with open(f"merged.json", "r+", encoding='utf-8') as f:
    data = json.load(f)
    for d in data['data']:
        details = {
            'typeCode': getValue(d, 'typeCode'),
            'estateName': getValue(d, 'estateName'),
            'phaseName': getValue(d, 'phaseName'),
            'address': getValue(d, 'address'),
            'nUnitPrice': getValue(d['sale'], 'nUnitPrice'),
            'postMinNUnitPrice': getValue(d['sale'], 'postMinNUnitPrice'),
            'postMaxNUnitPrice': getValue(d['sale'], 'postMaxNUnitPrice'),
            'unitPrice': getValue(d['sale'], 'nUnitPrice'),
            'postMinUnitPrice': getValue(d['sale'], 'postMinUnitPrice'),
            'postMaxUnitPrice': getValue(d['sale'], 'postMaxUnitPrice'),
            'minOpDate': getValue(d, 'minOpDate'),
            'maxOpDate': getValue(d, 'maxOpDate'),
            'phaseCount': getValue(d, 'phaseCount'),
            'buildingCount': getValue(d, 'buildingCount'),
            'unitCount': getValue(d, 'unitCount'),
        }
        master.append(details)

with open('analysed.csv', mode='w+', encoding='utf-8-sig', newline='') as f:
    keys = master[0].keys()
    writer = csv.DictWriter(f, keys)
    writer.writeheader()
    writer.writerows(master)