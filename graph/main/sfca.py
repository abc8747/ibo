import csv

from sqlalchemy.sql.operators import comma_op
from db import common

from rich import print, inspect
from rich.progress import track

with common.Session(common.engine) as session:
    samples = session.query(common.Sample).all()
    carparks = session.query(common.Carpark).all()
    population = session.query(common.Population).all()

newdata = [common.Sample.__csvHeaders__]
sfca = common.SFCA(samples=samples, carparks=carparks, population=population, carpark_catchment_distance=2250, population_catchment_distance=225).calculate()
for sample in samples:
    newdata.append(sample.genRow())
        
with open(f'out/sample_2catch.csv', 'w+', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(newdata)