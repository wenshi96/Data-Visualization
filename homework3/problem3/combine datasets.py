import os
import pandas as pd
value_fname = "cumulative-stats.tsv"
year_fname = "player-lookup.json"
path = os.getcwd()

value = pd.read_csv(os.path.join(path,value_fname),sep='\t')
year = pd.read_json(os.path.join(path,year_fname)).T

df = pd.merge(value,year)
df['age'] = df['year']-df['year_start']+df['age_start']

df.to_csv(os.path.join(path,"data.csv"))