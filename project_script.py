import os
import requests
import pandas as pd
from datetime import datetime
import datetime as date

# Download the data from https://api.covidtracking.com
path = os.path.abspath(os.path.dirname(__file__))
api = r'https://api.covidtracking.com/v1/states/daily.csv'

def get_statement(api, fname, path):
    response = requests.get(api)
    assert(fname.endswith('.csv')), 'Incorrect file type in get_statement, expected csv, got: {}'.format(api)
    with open(os.path.join(path, fname), 'wb') as file:
        file.write(response.content)

go_online = True # Change True if the file(s) not yet in the folder (see files)
fname = [] 
fname = api.split('/')[-1]
if go_online:
    get_statement(api, fname, path)

files = [file for file in os.listdir(path) if file.endswith('csv')]
keys = ['expire', 'nga', 'daily']

files = {k:v for k,v in zip(keys, files)}


# Compare table from NGA and Expire to get the latest reopening date
dfs = []
for k in files:
    if k in ['expire', 'nga']:
        df = pd.read_csv(files[k]) 
        dfs.append(df)
        
df = dfs[0].merge(dfs[1], on=['state'], how='left', 
                  indicator='exists')

df['Reopen date'] = pd.to_datetime(df['Reopen date'])
#df['expire_date'] = df['expire_date'].map('{} 20'.format)
#df['expire_date'] = df['expire_date'].astype('string')
df['expire_date'] = df.expire_date.apply(lambda x: pd.to_datetime(x).strftime('%M %d')[0])

for col in ['expire_date', 'Reopen date']:
    df[col] = pd.to_datetime(df[col])
    
    
# Graphs
