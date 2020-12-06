import os
import requests
import pandas as pd
import numpy as np
import us
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.gridspec as gridspec
import seaborn as sns
from datetime import datetime

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
    
# Compare table from NGA and expire to get the latest reopening date
files = ['state_expire_multistate.csv', 'table.csv', 'daily.csv']
keys = ['expire', 'nga', 'daily']
files = {k:v for k,v in zip(keys, files)}
 
def compare_date(key1, key2):
    dfs = []
    for k in files:
        if k in [key1, key2]:
            df = pd.read_csv(files[k]) 
            dfs.append(df)
    
    df = dfs[0].merge(dfs[1], on=['state'], how='left', 
                  indicator='exists')

    df['expire_date'] = df['expire_date'].map('{} 20'.format)
    
    for col in ['expire_date', 'Reopen date']:
        df[col] = pd.to_datetime(df[col], errors = 'coerce')
  
    df['policy_date'] = np.where((df['Reopen date'] > df['expire_date']), df['Reopen date'], df['expire_date'])
    df = df[['state', 'policy_date']].drop_duplicates(subset=['state'])
    return df

df_reopening = compare_date('expire', 'nga')     
df_reopening.to_csv('state_reopeningdate.csv', index=False)
    
# Read US Governor party csv data from github 
us_party = pd.read_csv('https://raw.githubusercontent.com/CivilServiceUSA/us-governors/master/us-governors/data/us-governors.csv')
us_party = us_party[['state_name', 'state_code', 'party']]
us_party.to_csv('us_party.csv', index=False)    
    
# Create dataframe containing state_id    
abbr = [state.abbr for state in us.states.STATES]
state = [state.name for state in us.states.STATES]
states_dict = {k:v for k,v in zip(abbr, state)}
states = pd.DataFrame(states_dict.items(), columns=['state_id', 'state'])
    
# Open daily data, create new column state for abbreviation
df_covid = pd.read_csv(files['daily'])
df_covid = df_covid[['date', 'state', 'positive', 'probableCases', 'negative']]
df_covid['date']=pd.to_datetime(df_covid['date'], format='%Y%m%d', errors = 'coerce')

df_covid = df_covid.merge(states, left_on=['state'], right_on=['state_id'], how='outer',
                          indicator=True)

# Merge with reopening policy date
df = df_covid.merge(df_reopening, left_on=['state_y'], right_on=['state'], how='outer',
                          indicator=False)

# Merge with governor's party 
df = df.merge(us_party, left_on=['state_y'], right_on=['state_name'], how='left', indicator=False)
col_drop = ['state_x', 'state_id', 'state_y', 'state', '_merge']
df.drop([col for col in df.columns if col in col_drop], axis=1, inplace=True)
df.to_csv('data.csv', index=False)    
    
# Creating Graphs
# Set earliest(1 March) and latest(30 November) date for each state

# 1) Average Comparison of The Number of Cases between Republican and Democrat States
df['tot_avg'] = df.groupby(['date', 'party'])['positive'].transform('mean')
df['new_cases'] = df.groupby(['state_name'])['positive'].diff(-1)
df['new_case_mean'] = df.groupby(['date', 'party'])['new_cases'].transform('mean')
df['new_cases_total'] = df.groupby(['date'])['new_cases'].transform('mean')
df['after_policy'] = (df['date'] > df['policy_date']).astype(int)
df['new_case_after'] = df.groupby(['state_name', 'after_policy'])['new_cases'].transform('mean')

# Add bar chart for average daily cases overall
fig, ax = plt.subplots(figsize=(15,7))
ax.set_title('Average Number of Covid-19 Daily Cases', fontsize=16)
ax.set_xlabel('Date', fontsize=14)
ax.set_ylabel('New Cases', fontsize=14)
ax.bar('date', 'new_cases_total', data = df, color='lightgray')
dstart = datetime(2020,4,1)
dend = datetime(2020,11,30)
ax.set_xlim([dstart, dend])
ax2 = ax.twinx()
ax2 = sns.lineplot(x='date', y='new_case_mean', hue='party', data = df, palette=['r', 'b'])
ax2.set_yticks([])
ax2.set_ylabel('')

# Try plot new_cases with vertical line
# Change df_reopening to dictionary
df_reopening = df_reopening.set_index('state')
reopening_dict = df_reopening['policy_date'].to_dict()

# filter top 5 states
top5 = df[['state_name', 'new_case_after', 'after_policy']].drop_duplicates()
print(top5[top5['after_policy']==1].nlargest(5, 'new_case_after'))
top5_state = ['California', 'Texas', 'Florida', 'Illinois', 'Ohio']
top5 = df.loc[df['state_name'].isin(top5_state)] 



fig, ax1 = plt.subplots(figsize=(12,7))
ax1.set_title('Average Number of Covid-19 Daily Cases', fontsize=16)
ax1.set_xlabel('Date', fontsize=14)
ax1.set_ylabel('New Cases', fontsize=14)
ax1 = sns.lineplot(x='date', y='new_cases', data = top5, hue = 'state_name')
ax1.axvline(datetime(2020,5,15), color="red", linestyle="--")





fig = plt.figure()
gs = gridspec.GridSpec(2, 2, hspace=0, wspace=0)
(ax1, ax2), (ax3, ax4) = gs.subplots(sharex='col', sharey='row')
fig.suptitle('Average Number of Covid-19 Daily Cases')
y1 = top5[top5['state_name']=='California'][['new_cases', 'date']]
ax1.plot('date', 'new_cases', data=y1)
y2 = top5[top5['state_name']=='Texas'][['new_cases', 'date']]
ax2.plot('date', 'new_cases', data=y2)
y3 = top5[top5['state_name']=='Florida'][['new_cases', 'date']]
ax3.plot('date', 'new_cases', data=y3)
y4 = top5[top5['state_name']=='Illinois'][['new_cases', 'date']]
ax4.plot('date', 'new_cases', data=y4)

