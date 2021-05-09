import csv
import hk80

with open(f"coords.csv", "r+", encoding='utf-8') as f:
    data = list(csv.reader(f))
