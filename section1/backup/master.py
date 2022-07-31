import urllib3
import json
from multiprocessing.dummy import Pool as ThreadPool
from pyproj import Transformer
import time

hk80_to_wgs84 = Transformer.from_crs("epsg:2326", "epsg:4326")
http = urllib3.PoolManager()
size = 10
def getKey(obj, key):
    return obj[key] if key in obj else ''
def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

# get all area codes. 23-WS000 #

# placeCodes = []
# areas = json.loads(http.request("GET", "https://hk.centanet.com/findproperty/api/Place/GetHmaPlaces").data.decode("utf-8"))

# placeCodes = [place['code'] for place in district['places'] for district in areas if "places" in district if place['code'][:2] == "23"]
# for district in areas:
#     if "places" in district:
#         for place in district['places']:
#             if place['code'][:2] == "23":
#                 placeCodes.append(place['code'])

placeCodes = ['23-WS017', '23-WS018', '23-WS019', '23-WS020', '23-WS021', '23-WS022', '23-WS023', '23-WS024', '23-WS025', '23-WS026', '23-WS027', '23-WS028', '23-WS029', '23-WS030', '23-WS031', '23-WS032', '23-WS033', '23-WS034', '23-WS035', '23-WS036', '23-WS037', '23-WS038', '23-WS039', '23-WS040', '23-WS041', '23-WS042', '23-WS043', '23-WS044', '23-WS045', '23-WS046', '23-WS047', '23-WS048', '23-WS049', '23-WS050', '23-WS051', '23-WS052', '23-WS053', '23-WS054', '23-WS055']
# placeCodes = ['23-WS001']

for placeCode in placeCodes:
    # probe for the number of results first.
    body = {"size": size, "sort": "NUnitPrice", "order": "Descending", "offset": 0, "typeCodes": [placeCode], "mtrs": [], "primarySchoolNets": []}
    count = json.loads(http.request("POST", "https://hk.centanet.com/findproperty/api/estate/Search", body=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json'}).data.decode("utf-8"))['count']
    offsets = [offset for offset in range(int(count/10)+1)]#[1]
    print(f"1: Probing found {count} buildings.")
    print(f"   Using 30 threads to request {len(offsets)} pages @ {size} results each...")

    # for each offset, get the data with multithreading.
    def getTypeCodes(offset):
        body = {"size": size, "sort": "NUnitPrice", "order": "Descending", "offset": offset, "typeCodes": [placeCode], "mtrs": [], "primarySchoolNets": []}
        data = json.loads(http.request("POST", "https://hk.centanet.com/findproperty/api/estate/Search", body=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json'}).data.decode("utf-8"))['data']
        return data

    pool = ThreadPool(30)
    rawResponses = pool.map(getTypeCodes, offsets)
    typeCodes = [r['typeCode'] for response in rawResponses for r in response]
    pool.close()
    pool.join()
    print(f"2: Retrieved {len(typeCodes)} buildings.")
    print(f"   Now sleeping for 10 seconds...")
    time.sleep(10)
    
    
    print(f"   Using 30 threads to request sale price information for each building, at 400 results/chunk...")
    def getDetails(typeCode):
        try:
            data = json.loads(http.request("GET", f"https://hk.centanet.com/estate/api/Estate/GetEstateDetail?typeCode={typeCode}&datasize=full").data.decode("utf-8"))
        except:
            data = {'map': {}, 'sale': {}}
            print(f'{typeCode} failed.')
        return {
            'typeCode': typeCode,
            'estateName': getKey(data, 'estateNameEN'),
            'phaseName': getKey(data, 'phaseNameEN'),
            'x': getKey(data['map'], 'lpt_x'),
            'y': getKey(data['map'], 'lpt_y'),
            'effective': getKey(data['sale'], 'nUnitPrice'),
            'effectiveMin': getKey(data['sale'], 'postMinNUnitPrice'),
            'effectiveMax': getKey(data['sale'], 'postMaxNUnitPrice'),
            'gross': getKey(data['sale'], 'unitPrice'),
            'grossMin': getKey(data['sale'], 'postMinUnitPrice'),
            'grossMax': getKey(data['sale'], 'postMaxUnitPrice'),
        }

    chunkedTypeCodes, chunksize = chunks(typeCodes, 400), int(len(typeCodes)/400)+1
    details = []
    for typeCodeChunkCounter, typeCodeChunk in enumerate(chunkedTypeCodes):
        print(f'   Requesting {typeCodeChunkCounter+1} / {chunksize} chunks...')
        pool = ThreadPool(30)
        details.extend(pool.map(getDetails, typeCodeChunk))
        pool.close()
        pool.join()
        print(f'   Done, sleeping for 10 seconds...')
        time.sleep(10)

    print(f"3: Finished retrieving information for all buildings.")
    print(f"   Using 30 threads to request building height and geometry on Gov API...")


    def getBuildingHeightAndGeometry(detail):
        yRaw, xRaw = detail['y'], detail['x']
        x, y = hk80_to_wgs84.transform(yRaw, xRaw)
        xMin, yMin = hk80_to_wgs84.transform(yRaw-200, xRaw-200)
        xMax, yMax = hk80_to_wgs84.transform(yRaw+200, xRaw+200)

        url = f'https://api.hkmapservice.gov.hk/ags/map/layer/ib1000//buildings/identify?key=6a40dd75bce8494ea735efd8d97dd820&f=json&tolerance=3&returnGeometry=true&imageDisplay=1000,1000,96&geometryType=esriGeometryPoint&geometry=%7B%22x%22%3A{y},%22y%22%3A{x}%7D&sr=4326&mapExtent={yMin},{xMin},{yMax},{xMax}'
        data = json.loads(http.request("GET", url).data.decode("utf-8"))['results']

        if data == []:
            detail['baseHeight'] = -1
            detail['roofHeight'] = -1
            detail['geometry'] = []
        else:
            # if 'Base Level' in data[0]:
            #     detail['baseHeight'] = data[0]['Base Level']
            # else:
            #     detail['baseHeight'] = data[0]['attributes']['Base Level'] if 'Base Level' in data[0]['attributes'] else -1

            # if 'Roof Level' in data[0]:
            #     detail['roofHeight'] = data[0]['Roof Level']
            # else:
            #     detail['roofHeight'] = data[0]['attributes']['Roof Level'] if 'Roof Level' in data[0]['attributes'] else -1
            
            detail['baseHeight'] = data[0]['Base Level'] if 'Base Level' in data[0] else data[0]['attributes']['Base Level'] if 'Base Level' in data[0]['attributes'] else -1
            detail['roofHeight'] = data[0]['Roof Level'] if 'Roof Level' in data[0] else data[0]['attributes']['Roof Level'] if 'Roof Level' in data[0]['attributes'] else -1
            detail['geometry'] = data[0]['geometry']['rings'][0] if 'geometry' in data[0] else []

        if detail['baseHeight'] == -1 or detail['roofHeight'] == -1 or detail['geometry'] == []:
            print(f"ERR: bh - {detail['baseHeight']}, rh - {detail['roofHeight']}, geo - {detail['geometry']} => {url}")
            print(f"________________________________________")
        return detail

    pool = ThreadPool(30)
    fullDetails = pool.map(getBuildingHeightAndGeometry, details)
    pool.close()
    pool.join()

    with open(f'data/{placeCode}.json', mode='w+', encoding='utf-8') as f:
        json.dump(fullDetails, f)