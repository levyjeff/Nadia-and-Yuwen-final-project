import os
import requests
import pandas as pd
from datetime import datetime
import datetime as date
import numpy as np
import us


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
    
# Read US Governor party csv data from github 
us_party = pd.read_csv('https://raw.githubusercontent.com/CivilServiceUSA/us-governors/master/us-governors/data/us-governors.csv')
us_party = us_party[['state_name', 'state_code', 'party']]
us_party.to_csv('us_party.csv', index=False)    
    
# Create dataframe containing state_id    
abbr = [state.abbr for state in us.states.STATES]
state = [state.name for state in us.states.STATES]
states = {k:v for k,v in zip(abbr, state)}
states = pd.DataFrame(states.items(), columns=['state_id', 'state'])
    
# Compare table from NGA and Expire to get the latest reopening date
files = [file for file in os.listdir(path) if file.endswith('csv')]
keys = ['expire', 'nga', 'daily']

files = {k:v for k,v in zip(keys, files)}

dfs = []
for k in files:
    if k in ['expire', 'nga']:
        df = pd.read_csv(files[k]) 
        dfs.append(df)
        
df = dfs[0].merge(dfs[1], on=['state'], how='left', 
                  indicator='exists')

df['expire_date'] = df['expire_date'].map('{} 20'.format)
    
for col in ['expire_date', 'Reopen date']:
    df[col] = pd.to_datetime(df[col], errors = 'coerce')

    
df['policy_date'] = np.where((df['Reopen date'] > df['expire_date']), df['Reopen date'], df['expire_date'])
df = df[['state', 'policy_date']].drop_duplicates(subset=['state'])
df.to_csv('state_reopeningdate.csv', index=False)

# Open daily data, create new column state for abbreviation

    
# Graphs
