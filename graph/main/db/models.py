from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import csv
from rich import print, inspect

Base = declarative_base()
engine = create_engine('sqlite:///data.db', echo=False)

class Sample(Base):
    __tablename__ = "samples"

    sample_id = Column('sample_id', String, primary_key=True, index=True)
    x = Column('x', Float)
    y = Column('y', Float)
    accessibility = Column('accessibility', Float)

    def genRow(self):
        return (self.sample_id, self.x, self.y, self.accessibility)

class Population(Base):
    __tablename__ = "population"

    building_id = Column('building_id', String, primary_key=True, index=True)
    typeofbuilding = Column('typeofbuilding', String)
    height = Column('height', Float)
    floor = Column('floor', Integer)
    gfa = Column('gfa', Integer)
    x = Column('x', Float)
    y = Column('y', Float)

    def genRow(self):
        return (self.building_id, self.typeofbuilding, self.height, self.floor, self.gfa, self.x, self.y)

class PopulationMatrix(Base):
    __tablename__ = "populationMatrix"

    pk = Column('pk', Integer, primary_key=True, autoincrement=True)
    origin_id = Column('origin_id', String, index=True)
    destination_id = Column('destination_id', String, index=True)
    entry_cost = Column('entry_cost', Float)
    network_cost = Column('network_cost', Float)
    exit_cost = Column('exit_cost', Float)
    total_cost = Column('total_cost', Float)

    def genRow(self):
        return (self.origin_id, self.destination_id, self.entry_cost, self.network_cost, self.exit_cost, self.total_cost)

class Carpark(Base):
    __tablename__ = "carpark"

    carpark_id = Column('carpark_id', String, primary_key=True, index=True)
    description = Column('description', String)
    source = Column('source', String)
    gfa = Column('gfa', Integer)
    type = Column('type', String)
    amount = Column('amount', Integer)
    x = Column('x', Float)
    y = Column('y', Float)

    def genRow(self):
        return (self.carpark_id, self.description, self.source, self.gfa, self.type, self.amount, self.x, self.y)

class CarparkMatrix(Base):
    __tablename__ = "carparkMatrix"

    pk = Column('pk', Integer, primary_key=True, autoincrement=True)
    origin_id = Column('origin_id', String, index=True)
    destination_id = Column('destination_id', String, index=True)
    entry_cost = Column('entry_cost', Float)
    network_cost = Column('network_cost', Float)
    exit_cost = Column('exit_cost', Float)
    total_cost = Column('total_cost', Float)

    def genRow(self):
        return (self.origin_id, self.destination_id, self.entry_cost, self.network_cost, self.exit_cost, self.total_cost)

Base.metadata.create_all(engine)

# automatically insert data if not present.
with Session(engine) as session:
    if not session.query(Sample).count():
        print("Inserting sample...")
        with open(f'samples.csv', 'r', encoding='utf-8-sig', newline='') as f:
            data = list(csv.reader(f))[1:]
            session.bulk_save_objects([Sample(**{
                "sample_id": d[0],
                "x": d[1],
                "y": d[2],
            }) for d in data])

    if not session.query(Population).count():
        print("Inserting population...")
        with open(f'populations.csv', 'r', encoding='utf-8-sig', newline='') as f:
            data = list(csv.reader(f))[1:]
            session.bulk_save_objects([Population(**{
                "building_id": d[0],
                "typeofbuilding": d[2],
                "height": float(d[3]) if d[3] else 0,
                "floor": int(d[4]) if d[4] else 0,
                "gfa": int(d[5]) if d[5] else 0,
                "x": float(d[6]),
                "y": float(d[7]),
            }) for d in data])

    if not session.query(PopulationMatrix).count():
        print("Inserting population matrix...")
        with open(f'population_matrix.csv', 'r', encoding='utf-8-sig', newline='') as f:
            data = list(csv.reader(f))[1:]
            session.bulk_save_objects([PopulationMatrix(**{
                "origin_id": d[0],
                "destination_id": d[1],
                "entry_cost": float(d[2]),
                "network_cost": float(d[3]),
                "exit_cost": float(d[4]),
                "total_cost": float(d[5]),
            }) for d in data])

    if not session.query(Carpark).count():
        print("Inserting carpark...")
        with open(f'carparks.csv', 'r', encoding='utf-8-sig', newline='') as f:
            data = list(csv.reader(f))[1:]
            session.bulk_save_objects([Carpark(**{
                "carpark_id": d[0],
                "description": d[1],
                "source": d[2],
                "gfa": int(d[3]) if d[3] else 0,
                "type": d[4],
                "amount": int(d[5]) if d[4] else 0,
                "x": float(d[6]),
                "y": float(d[7]),
            }) for d in data])

    if not session.query(CarparkMatrix).count():
        print("Inserting car parks matrix...")
        with open(f'carpark_matrix.csv', 'r', encoding='utf-8-sig', newline='') as f:
            data = list(csv.reader(f))[1:]
            session.bulk_save_objects([CarparkMatrix(**{
                "origin_id": d[0],
                "destination_id": d[1],
                "entry_cost": float(d[2]),
                "network_cost": float(d[3]),
                "exit_cost": float(d[4]),
                "total_cost": float(d[5]),
            }) for d in data])

    session.commit()