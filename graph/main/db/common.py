from rich import print, inspect
from rich.progress import track
import math

from sqlalchemy.sql.coercions import WhereHavingImpl
from .models import *
from time import time_ns
from sqlalchemy.sql import select

class SFCA:
    def __init__(self, samples, carparks, population, catchment_distance):
        self.samples = samples
        self.carparks = carparks
        self.population = population
        self.catchment_distance = catchment_distance
    
    def decay(self, distance):
        if distance < self.catchment_distance:
            return (math.exp(-0.5*(math.pow((distance/self.catchment_distance), 2))) - math.exp(-0.5)) / (1-math.exp(-0.5))
        return 0

    def calculate(self):
        with Session(engine) as session:
            for sample in self.samples:
                try:
                    start = time_ns()
                    sample.accessibility = 0
                    for carpark in self.carparks:
                        d = session.execute(select(CarparkMatrix.total_cost).where((CarparkMatrix.origin_id == sample.sample_id) & (CarparkMatrix.destination_id == carpark.carpark_id))).fetchone()[0]
                        if d is None: continue
                        supply = carpark.amount * self.decay(d)

                        demand = 0
                        for gfa, distance in session.execute(select(Population.gfa, PopulationMatrix.total_cost).where(PopulationMatrix.origin_id == carpark.carpark_id).join(Population, PopulationMatrix.destination_id == Population.building_id)):
                            if distance is None: continue
                            demand += gfa * self.decay(distance)

                        sample.accessibility += supply / demand
                    print(sample.sample_id, '->', (time_ns() - start) / 1e9)
                except Exception:
                    pass