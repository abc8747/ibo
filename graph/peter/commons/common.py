import requests
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyDkvo7O65VGJZeQ-EneJZjIdOMMKC8yGv4')

class Location:
    def __init__(self, locationid:int, description:str=None, address:str=None, lat:float=None, lon:float=None, number:int=None):
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