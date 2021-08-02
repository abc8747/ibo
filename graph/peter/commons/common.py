from os import name
import requests
import googlemaps
from pyproj import Transformer, Proj

gmaps = googlemaps.Client(key='AIzaSyDkvo7O65VGJZeQ-EneJZjIdOMMKC8yGv4')
hk80_to_wgs84 = Transformer.from_crs("epsg:2326", "epsg:4326").transform
wgs84_to_hk80 = Transformer.from_crs("epsg:4326", "epsg:2326").transform
hk80 = Proj('epsg:2326')
wgs84 = Proj('epsg:4326')

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
        except:
            pass

        return self
    
    def genRow(self):
        return [self.locationid, self.name, self.query, self.number, self.address, self.lat, self.lon, self.placeid]