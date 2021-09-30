import os
from rich import print, inspect
import pandas as pd

class Survey:
    def __init__(self, surveyid, data):
        self.surveyid = surveyid
        self.data = data

        self.total_occupied_duration = sum(self.data.iloc[i+1].t - self.data.iloc[i].t for i in range(len(self.data)-1) if self.data.iloc[i].state == 1 and self.data.iloc[i+1].state == 0)
        self.total_duration = self.data.iloc[-1].t
        self.vehicle_count = sum(1 for d in self.data.itertuples() if d.state == 1)

        self.occupancy = self.total_occupied_duration / self.total_duration
        self.flow = self.vehicle_count / (self.total_duration / 3600) # veh/hr
        self.relativeSpeed = self.flow / self.occupancy

sfca_df = pd.read_csv('out/sample_survey.csv', index_col='sample_id')

surveys = []
for filename in os.listdir('survey/raw/json'):
    survey_processed = Survey(filename.split('.')[0], pd.read_json(os.path.join('survey/raw/json', filename)))
    survey_sfca = sfca_df.loc[int(survey_processed.surveyid)]
    surveys.append([survey_processed.surveyid] + survey_sfca.values.tolist() + [survey_processed.occupancy, survey_processed.flow, survey_processed.relativeSpeed])

df = pd.DataFrame(surveys, columns=['id', *sfca_df, 'occupancy', 'flow', 'relativeSpeed'])
df.to_csv('out/processed_survey.csv', index=False)