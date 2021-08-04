import googlemaps
from pyproj import Transformer, Proj
from rich import print, inspect
from rich.progress import track
import math

gmaps = googlemaps.Client(key='AIzaSyDkvo7O65VGJZeQ-EneJZjIdOMMKC8yGv4')
hk80_to_wgs84 = Transformer.from_crs("epsg:2326", "epsg:4326").transform
wgs84_to_hk80 = Transformer.from_crs("epsg:4326", "epsg:2326").transform
hk80 = Proj('epsg:2326')
wgs84 = Proj('epsg:4326')

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class Coordinate:
    def __init__(self, lat=None, lon=None, x=None, y=None, autoconvert=True):
        self.lat = float(lat) if lat else None
        self.lon = float(lon) if lon else None
        self.x = float(x) if x else None
        self.y = float(y) if y else None

        if autoconvert:
            if self.x is None and self.y is None:
                self.getHK80()
            if self.lat is None and self.lon is None:
                self.getWGS84()
    
    def getWGS84(self):
        if self.x and self.y:
            self.lat, self.lon = hk80_to_wgs84(self.y, self.x)
    
    def getHK80(self):
        if self.lat and self.lon:
            self.y, self.x = wgs84_to_hk80(self.lat, self.lon)

    def getDistance(self, coordinate):
        return math.sqrt(
            math.pow(self.x - coordinate.x, 2) + math.pow(self.y - coordinate.y, 2)
        )

class Location:
    csvheaders = ['locationid', 'name', 'query', 'number', 'address', 'lat', 'lon', 'placeid']

    def __init__(self, locationid, name, query, number, address=None, lat=None, lon=None, placeid=None):
        self.locationid = int(locationid)
        self.name = name
        self.query = query
        self.number = int(number)

        self.address = address
        self.coords = Coordinate(lat=float(lat) if lat else None, lon=float(lon) if lon else None)
        self.placeid = placeid

    def geocode(self):
        try:
            self._geocode_result = gmaps.geocode(self.query)[0]

            self.address = self._geocode_result["formatted_address"]
            self.coords = Coordinate(
                lat=self._geocode_result["geometry"]["location"]["lat"], 
                lon=self._geocode_result["geometry"]["location"]["lng"]
            )
            self.placeid = self._geocode_result["place_id"]
        except Exception as e:
            print(e)

        return self
    
    def genRow(self):
        return [self.locationid, self.name, self.query, self.number, self.address, self.coords.lat, self.coords.lon, self.placeid]

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

# sfca

class Building:
    csvheaders = ['buildingid','gfa','height','x','y']

    def __init__(self, buildingid, gfa, height, x, y):
        self.buildingid = buildingid
        self.gfa = float(gfa)
        self.height = float(height)
        self.coords = Coordinate(x=x, y=y)

class Sample:
    csvheaders = ['sampleid','x','y']

    def __init__(self, sampleid, x, y):
        self.sampleid = sampleid
        self.coords = Coordinate(x=x, y=y)
        self.accessibility = 0

    def genRow(self):
        return [self.sampleid, self.coords.x, self.coords.y, self.accessibility]

class SFCA:
    def __init__(self, samples, locations, buildings, catchment_distance):
        self.samples = samples
        self.locations = locations
        self.buildings = buildings
        self.catchment_distance = catchment_distance
    
    def decay(self, distance):
        if distance < self.catchment_distance:
            return (math.exp(-0.5*(math.pow((distance/self.catchment_distance), 2))) - math.exp(-0.5)) / (1-math.exp(-0.5))
        return 0

    def calculate(self):
        for sample in self.samples:
            sample.accessibility = 0
            for location in self.locations:
                demand = 0
                for building in self.buildings:
                    demand += building.gfa * self.decay(location.coords.getDistance(building.coords))
                supply = location.number * self.decay(sample.coords.getDistance(location.coords))
                sample.accessibility += supply / demand
            
            if int(sample.sampleid) % 10 == 0:
                print(sample.sampleid)
        return self

# def f(D_ij, D_0):
#     if D_ij < D_0:
#         return (math.exp(-0.5*(math.pow((D_ij/D_0), 2))) - math.exp(-0.5)) / (1-math.exp(-0.5))
#     else:
#         return 0