from os import name
import requests
import googlemaps
from pyproj import Transformer, Proj
from rich import print, inspect
from rich.progress import track

gmaps = googlemaps.Client(key='AIzaSyDkvo7O65VGJZeQ-EneJZjIdOMMKC8yGv4')
hk80_to_wgs84 = Transformer.from_crs("epsg:2326", "epsg:4326").transform
wgs84_to_hk80 = Transformer.from_crs("epsg:4326", "epsg:2326").transform
hk80 = Proj('epsg:2326')
wgs84 = Proj('epsg:4326')

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class Coordinate:
    def __init__(self, lat=None, lon=None, x=None, y=None):
        self.lat = float(lat) if lat else None
        self.lon = float(lon) if lon else None
        self.x = float(x) if x else None
        self.y = float(y) if y else None

        if self.x is None and self.y is None:
            self.getHK80()
        if self.lat is None and self.lon is None:
            self.getWGS84()
    
    def getWGS84(self):
        self.lat, self.lon = hk80_to_wgs84(self.x, self.y)
    
    def getHK80(self):
        self.x, self.y = wgs84_to_hk80(self.lat, self.lon)

class Location:
    csvheaders = ['locationid', 'name', 'query', 'number', 'address', 'lat', 'lon', 'placeid']

    def __init__(self, locationid, name, query, number, address=None, lat=None, lon=None, placeid=None):
        self.locationid = int(locationid)
        self.name = name
        self.query = query
        self.number = int(number)

        self.address = address
        self.lat = float(lat) if lat else None
        self.lon = float(lon) if lon else None
        self.placeid = placeid

    def geocode(self):
        try:
            self._geocode_result = gmaps.geocode(self.query)[0]

            self.address = self._geocode_result["formatted_address"]
            self.lat = self._geocode_result["geometry"]["location"]["lat"]
            self.lon = self._geocode_result["geometry"]["location"]["lng"]
            self.placeid = self._geocode_result["place_id"]
        except Exception as e:
            print(e)

        return self
    
    def genRow(self):
        return [self.locationid, self.name, self.query, self.number, self.address, self.lat, self.lon, self.placeid]

class Route:
    def __init__(self, origin_locationid, destination_locationid, distance, duration):
        self.origin_locationid = origin_locationid
        self.destination_locationid = destination_locationid
        self.distance = distance
        self.duration = duration
    
    def genRow(self):
        return [self.origin_locationid, self.destination_locationid, self.distance, self.duration]

class Routes:
    csvheaders = ['originid', 'destinationid', 'distance', 'duration']

    def __init__(self, locations):
        self.locations = [Location(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7]) for l in locations]

    def getRoutes(self):
        self.routes = [Routes.csvheaders]
        c0 = 0
        for origin in self.locations:
            c1 = 0
            for chunked_destinations in chunks(list(filter(lambda e:e.locationid != origin.locationid, self.locations)), 25):
                print(f'Requesting origin {c0} chunk {c1}.')
                try:
                    destination_locationids = [d.locationid for d in chunked_destinations]
                    routes = gmaps.distance_matrix(
                        origins=f'place_id:{origin.placeid}',
                        destinations=[f'place_id:{d.placeid}' for d in chunked_destinations],
                        mode='walking'
                    )
                    for i, r in enumerate(routes["rows"][0]["elements"]):
                        self.routes.append(Route(origin.locationid, destination_locationids[i], r["distance"]["value"], r["duration"]["value"]).genRow())
                except Exception as e:
                    print(e)
                c1 += 1
            c0 += 1
        
        return self