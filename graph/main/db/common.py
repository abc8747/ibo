import math
from pyproj import Transformer, Proj
from rich import print, inspect
from rich.progress import Progress
from .models import *

from sqlalchemy.sql import select

hk80_to_wgs84 = Transformer.from_crs("epsg:2326", "epsg:4326").transform
wgs84_to_hk80 = Transformer.from_crs("epsg:4326", "epsg:2326").transform
hk80 = Proj('epsg:2326')
wgs84 = Proj('epsg:4326')

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

class SFCA:
    def __init__(self, samples, carparks, population, carpark_catchment_distance, population_catchment_distance):
        self.samples = samples
        self.carparks = carparks
        self.population = population
        self.carpark_catchment_distance = carpark_catchment_distance
        self.population_catchment_distance = population_catchment_distance
    
    def decayCarpark(self, distance):
        if distance < self.carpark_catchment_distance:
            return (math.exp(-0.5*(math.pow((distance/self.carpark_catchment_distance), 2))) - math.exp(-0.5)) / (1-math.exp(-0.5))
        return 0

    def decayPopulation(self, distance):
        if distance < self.population_catchment_distance:
            return (math.exp(-0.5*(math.pow((distance/self.population_catchment_distance), 2))) - math.exp(-0.5)) / (1-math.exp(-0.5))
        return 0

    def calculate(self):
        with Session(engine) as session, Progress() as progress:
            sfcatask = progress.add_task("[yellow]Running SFCA...", total=len(self.samples))
            for sample in self.samples:
                try:
                    sample.accessibility = 0
                    for carpark in self.carparks:
                        d = session.execute(select(CarparkMatrix.total_cost).where((CarparkMatrix.origin_id == sample.sample_id) & (CarparkMatrix.destination_id == carpark.carpark_id))).fetchone()[0]
                        if d is None: continue
                        supply = carpark.amount * self.decayCarpark(d)

                        demand = 0
                        for gfa, distance in session.execute(select(Population.gfa, PopulationMatrix.total_cost).where(PopulationMatrix.origin_id == carpark.carpark_id).join(Population, PopulationMatrix.destination_id == Population.building_id)):
                            if distance is None: continue
                            demand += gfa * self.decayPopulation(distance)
                        
                        if demand == 0: continue
                        sample.accessibility += supply / demand
                except Exception:
                    pass
                finally:
                    progress.update(sfcatask, advance=1)
        
        return self