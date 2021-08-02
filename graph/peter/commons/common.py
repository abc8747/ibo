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
    def __init__(self, locationid, description=None, address=None, lat=None, lon=None, number=None):
        self.locationid = int(locationid)
        self.description = description
        self.address = address
        self.lat = float(lat) if lat else None
        self.lon = float(lon) if lon else None
        self.number = int(number) if number else None
        self.geocode_result = None

    def geocode(self, querydata:str):
        self.geocode_result = gmaps.geocode(querydata)
    
    # def getLocations(self, querydata:str):
    #     self._locations = requests.get(f'https://www.als.ogcio.gov.hk/lookup?q={querydata}', headers={
    #         'Accept': 'application/json'
    #     }).json()
    #     self._locations = self._locations['SuggestedAddress'] if self._locations else []
    #     return self
    
    # def setLocation(self, index:int=None):
    #     if index is None:
    #         for index, l in enumerate(self._locations):
    #             if l["Address"]["PremisesAddress"]["EngPremisesAddress"]["EngDistrict"]["DcDistrict"] == 'WONG TAI SIN DISTRICT':
    #                 break
    #         else:
    #             index = 0

    #     selected = self._locations[index]
    #     if not self.address:
    #         street = selected["Address"]["PremisesAddress"]["EngPremisesAddress"]["EngStreet"]
    #         self.address = f'{street["BuildingNoFrom"]} {street["StreetName"]}'
    #     if not self.description:
    #         self.description = selected["Address"]["PremisesAddress"]["EngPremisesAddress"]["BuildingName"]
    #     if not self.lat:
    #         self.lat = float(selected["Address"]["PremisesAddress"]["GeospatialInformation"]["Latitude"])
    #     if not self.lon:
    #         self.lon = float(selected["Address"]["PremisesAddress"]["GeospatialInformation"]["Longitude"])
        
    #     return self