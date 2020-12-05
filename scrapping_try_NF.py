import requests

# Web scrapping: reopening policy from https://www.huschblackwell.com/state-by-state-covid-19-guidance
# Note to the link we we pick a state: https://www.huschblackwell.com/illinois-state-by-state-covid-19-guidance
# state name is inserted after '/' before 'state' with '-'
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os

# I tried with one url first, haven't iterate over several urls
path = os.path.abspath(os.path.dirname(__file__))
urls = []
url = r'https://www.huschblackwell.com/illinois-state-by-state-covid-19-guidance'
head = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

resp = requests.get(url, headers=head)
soup = BeautifulSoup(resp.text, 'html.parser')

# reopen may be within li or p
# maybe not reopen but Phase 4
def keyword_idx(self):
    idx = []
    keyword = ['reopen', 'reopening', 'in-person', 'Phase 4']

    for i, elem in enumerate(self):
        for w in keyword:
            if w in elem.text:
                idx.append(i)
            else:
                pass
    return idx

# get the web content
divs = soup.findAll('div', attrs={ "class" : "wb-content"})

# Find the index of Phase 4 in p
for div in divs:
     idx_p = keyword_idx(div.find_all('p'))
idx_p = list(set(idx_p))
idx_p.sort()
     
# P_desc return list
p_descs = []
for div in divs:
    p_text = div.find_all('p')
    p_descs.extend([p.text for p in p_text])
p_descs = [s.replace('\xa0', ' ') for s in p_descs]
p_descs = [s.replace(':', '') for s in p_descs]

# Get the index for each date
idx_date = []
for i, s in enumerate(p_descs):
   if len(s.split()) == 3:
      idx_date.append(i)
    
# What you want is getting the date before the announcement
idx_before = []
for n in idx_p:
    idx_before.append(n-1)
    idx_before.append(n-2)
    idx_before.append(n-3)

# Keep only date index before the announcement
idx_fin = list(set(idx_date).intersection(set(idx_before)))
idx_fin.sort()

# How about only keeping the date right before
for n,m in zip(idx_p, idx_date):
    if m == n-1:
        idx_date.remove(m)
        
#concenate the index
idx = idx_fin + idx_p
idx.sort()

p = []
for i in idx:
    p.append(p_descs[i])
    
# stupid step: get the date from the max index in index_fin, that is the date for the state




# Scrapping from NGA
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
    
    df = pd.DataFrame({'State':col1, 'Reopen date': col2})
    for col in df.columns:
        df[col] = df[col].str.rstrip('\n')
        df[col] = df[col].str.rstrip(' ')
        
    return df

table = get_table("column-1", "column-3")
table.to_csv('table.csv', index=False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

