import csv

from sqlalchemy.sql.operators import comma_op
from db import common
# from db import models

from rich import print, inspect
from rich.progress import track

from db.models import Population

with common.Session(common.engine) as session:
    samples = session.query(common.Sample).all()
    carparks = session.query(common.Carpark).all()
    population = session.query(common.Population).all()

newdata = [common.Sample.__csvHeaders__]
sfca = common.SFCA(samples=samples, carparks=carparks, population=population, catchment_distance=1000).calculate()
for sample in samples:
    newdata.append(sample.genRow())
        
with open(f'out/sample.csv', 'w+', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(newdata)