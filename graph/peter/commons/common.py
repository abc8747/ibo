import requests

class Location:
    def __init__(self, description=None, address=None, lat=None, lon=None):
        self.description = description
        self.address = address
        self.lat = lat
        self.lon = lon
        self.locations = []
    
    def getLocations(self, data):
        self.locations = requests.get(f'https://www.als.ogcio.gov.hk/lookup?q={data}', headers={
            'Accept': 'application/json'
        }).json()['SuggestedAddress']
        return self

    def printLocations(self):
        print(self.locations)
        return self
    
    def setLocation(self, index:int):
        selected = self.locations[index]
        if not self.address:
            street = selected["Address"]["EngPremisesAddress"]["EngStreet"]
            self.address = f'{street["BuildingNoFrom"]} {street["StreetName"]}'

        return self