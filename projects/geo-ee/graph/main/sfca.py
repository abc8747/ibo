from db import common
import pandas as pd

from rich import print, inspect
from rich.progress import track

with common.Session(common.engine) as session:
    samples = session.query(common.Sample).all()
    carparks = session.query(common.Carpark).all()
    population = session.query(common.Population).all()

survey_ids = ('632', '1804', '105', '2354', '2175', '22', '1700', '1283', '2308', '2252', '239', '2328', '1823', '841', '433', '2491', '1495', '458', '1075', '2481', '2979', '2062', '1735', '2567', '138', '2373', '2201', '2643', '159', '290', '1336', '212', '2041', '2004', '394', '2665', '2694', '1107', '2417', '589', '1899', '1850', '2549', '2091', '2513', '1904', '1868', '1261', '1938', '1754', '2716', '2437', '1210', '49', '2461', '499', '1015', '2131', '2393', '2595', '1375', '421')
carpark_catchment_distance = 972
population_catchment_distance = 181.83

sfca = common.SFCA(samples=samples, carparks=carparks, population=population, carpark_catchment_distance=carpark_catchment_distance, population_catchment_distance=population_catchment_distance).calculate()
df = pd.DataFrame([sample.genRow() for sample in sfca.samples], columns=common.Sample.__csvHeaders__)
df.to_csv('out/sample.csv', index=False)

sfca = common.SFCA(samples=[s for s in samples if s.sample_id in survey_ids], carparks=carparks, population=population, carpark_catchment_distance=carpark_catchment_distance, population_catchment_distance=population_catchment_distance).calculate()
df = pd.DataFrame([sample.genRow() for sample in sfca.samples], columns=common.Sample.__csvHeaders__)
df.to_csv('out/sample_survey.csv', index=False)