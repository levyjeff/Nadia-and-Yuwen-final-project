# This is a file that includes all the downloading and webscraping

import os
import requests
import pandas as pd
import numpy as np
import us
from bs4 import BeautifulSoup
import re


os.getcwd()
path_with_os = os.path.expanduser(r'~\Documents\GitHub\Nadia-and-Yuwen-final-project')

######## I. Webscraping dates when stay-at-home order expired
head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
# need change according to your own device


## 1. NGA dataset
# Web Scraping from NGA 
nga = r'https://www.nga.org/coronavirus-reopening-plans/'       
resp1 = requests.get(nga, headers=head)
soup1 = BeautifulSoup(resp1.text, 'html.parser')

# Function for scrapping
def get_table(col1, col2):
    col1 = soup1.findAll('td', attrs={ "class" : col1})
    col1_descs = []
    for c in col1:
        col1_descs.extend([c.text for c in col1])
    col1 = col1_descs[0:43]

    col2 = soup1.findAll('td', attrs={ "class" : col2})
    col2_descs = []
    for c in col2:
        col2_descs.extend([c.text for c in col2])
    col2 = col2_descs[0:43]
    
    df = pd.DataFrame({'state':col1, 'Reopen date': col2})
    for col in df.columns:
        df[col] = df[col].str.rstrip('\n')
        df[col] = df[col].str.rstrip(' ')
        
    return df

table = get_table("column-1", "column-3")
table.to_csv('table.csv', index=False)

# After checking NGA dataset, we found that most states have missing dates
# So we find another website containing better data

## 2. Web scrapping: stay-at-home order expire date from MULTISTATE
# Source: https://docs.google.com/document/u/1/d/e/2PACX-1vSXZCFCbIRiRDRC-SWyc36T0S0hjXxT9wZAGM4V01_xtbywLBEn0o_kgmfs0dMJ4VbpPh30j2ZFZ3TH/pub
stayhome_order = r'https://docs.google.com/document/u/1/d/e/2PACX-1vSXZCFCbIRiRDRC-SWyc36T0S0hjXxT9wZAGM4V01_xtbywLBEn0o_kgmfs0dMJ4VbpPh30j2ZFZ3TH/pub'
resp2 = requests.get(stayhome_order, headers=head)
soup2 = BeautifulSoup(resp2.text, 'html.parser')        
        
# get the web content
# get all states
states = []
index = []
h3 = soup2.find_all("h3")    
for i in range(len(h3)):
    a = h3[i].find_all("a")
    if len(a) != 0:
        state = a[0].text
        states.append(state)
        index.append(i)
    else:
        continue

# get all expire related content for all states
expire_date = []
for i in index:
    ul = h3[i].find_next("ul")
    spans = ul.find_all("span")
    expire = [span.text for span in spans]
    expire_date.append(expire)

#merge state with its stay-home policy expire date
state_expire = pd.DataFrame(
    {'state': states,
     'expire': expire_date,
    })      

#remove counties
state_expire = state_expire.head(44)
#get the latest date for stay-at-home order to expire
last_dates = []
for ele in state_expire['expire']:
    dates = []
    
    for li in ele:
        date = re.findall('[a-zA-Z]{3,9}?\s\d+', li)
        if len(date) != 0:
            dates.append(date[0])
    last_date = dates[-1]
    last_dates.append(last_date)
    
#merge the date with dataframe
state_expire['expire_date'] = last_dates
        
# some states have text that confused with the date
# we need to manually change it
state_expire['expire_date'][16] = "May 31" 
state_expire['expire_date'][31] = "Apr 30"     
state_expire['expire_date'][40] = "May 29"         
state_expire['expire_date'][3] = "May 4"  

#keep only state and expire_date
state_expire  = state_expire.drop('expire', 1)

#we found some states are missing in our dataframe
#get the us_state list
us_state = [state.name for state in us.states.STATES]
# find which states are missing in state_expire_multistate.csv
missing_state = []
for item in us_state:
    if item not in state_expire['state'].tolist():
        missing_state.append(item)

missing_state_expire_date = ["May4", "Jun 1", "Jun 1", "May 1", "Apr 28", "Apr 30"]
#Those are the dates that we manually get from website seperately
#We tried to use NLP/keyword index, but it's not accurate and not efficient
#All states have their own wording in giving out the orders

missing_state_expire = pd.DataFrame(
    {'state': missing_state,
     'expire_date': missing_state_expire_date,
    })

state_expire = state_expire.append(missing_state_expire, ignore_index=True)

#save to csv
state_expire.to_csv(path_or_buf = os.path.join(path_with_os, 'state_expire_multistate.csv'),  index = False)

################################


######## II. downloading dataset from online

## 1. Download the data from https://api.covidtracking.com

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
    get_statement(api, fname, path_with_os)
    
## 2. Compare table from NGA and multistate_expire to get the latest reopening date
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
df_reopening['policy_date']=pd.to_datetime(df_reopening['policy_date'], format='%Y-%m-%d', errors = 'coerce') 
df_reopening.to_csv('state_reopeningdate.csv', index=False)

## 3. Download Party dateset
# Read US Governor party csv data from github 
us_party = pd.read_csv('https://raw.githubusercontent.com/CivilServiceUSA/us-governors/master/us-governors/data/us-governors.csv')
us_party = us_party[['state_name', 'state_code', 'party']]
us_party.to_csv('us_party.csv', index=False)    
    
## 4. Merge and create final dataset: data.csv
#Create dataframe containing state_id    
abbr = [state.abbr for state in us.states.STATES]
us_state = [state.name for state in us.states.STATES]
states_dict = {k:v for k,v in zip(abbr, us_state)}
states = pd.DataFrame(states_dict.items(), columns=['state_id', 'state'])
    
# Open daily data, create new column state for abbreviation
df_covid = pd.read_csv(files['daily'])
df_covid = df_covid[['date', 'state', 'positive', 'probableCases', 'negative', 'death']]
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

