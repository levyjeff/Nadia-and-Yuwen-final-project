import requests

# Web scrapping: reopening policy from https://www.huschblackwell.com/state-by-state-covid-19-guidance
# Note to the link we we pick a state: https://www.huschblackwell.com/illinois-state-by-state-covid-19-guidance
# state name is inserted after '/' before 'state' with '-'
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# I tried with one url first, haven't iterate over several urls
path = os.path.abspath(os.path.dirname(__file__))
urls = []
url = r'https://www.huschblackwell.com/illinois-state-by-state-covid-19-guidance'
head = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

resp = requests.get(url, headers=head)
soup = BeautifulSoup(resp.text, 'html.parser')

# reopen may be within li or p
# maybe not reopen but Phase 4
idx = []
def indices(self):
    for i, elem in enumerate(self): #https://stackoverflow.com/questions/5466618/too-many-values-to-unpack-iterating-over-a-dict-key-string-value-list
        if 'Phase 4' in elem.text:
            idx.append(i)
        elif 'phase 4' in elem.text:
            idx.append(i)
    return idx

# get the web content
divs = soup.findAll('div', attrs={ "class" : "wb-content"})

# Find the index of Phase 4 in p
for div in divs:
     idx_p = indices(div.find_all('p'))
     idx_p.sort()
     
# P_desc return list
p_descs = []
for div in divs:
    p_text = div.find_all('p')
    p_descs.extend([p.text for p in p_text])
p_descs = [s.replace('\xa0', ' ') for s in p_descs]
p_descs = [s.replace(':', '') for s in p_descs]
p_descs = p_descs.astype('string')

# Get the index for each date
for s in p_descs :
   if len(s.split()) == 3:
      print(s)

# Work to get paragraph with phase 4, need to get the date -> still fail since the date is also inside <p>
# Maybe use keyword to indicate that we want the date?

import datetime as dt
#p_descs['date'] = datetime.strptime(p_descs['text'],'%B %d, %Y')
#p_descs['date'] = p_descs['date'].strftime('%Y-%m-%d')

p_phase4 = []
for i in idx_p:
    p_phase4.append(p_descs[i-1])
 
# We might need to do NPL to get that the state moves into phase 4?
    
# Try to put the words into a dataframe instead of list, or a dictionary?
# Make a new column, containing different numbers at each date, then fill the rest of the rows with the same numbers
# If Phase 4 is inside then, we keep the 1st row and the row in which the phrase is contained
p_descs = pd.DataFrame()
for div in divs:
    p_descs['text'] = div.find_all('p')

p_descs['string'] = [" ".join(map(str, l)) for l in p_descs['text']]
# strip <strong> and :</strong>
p_descs['string'] = p_descs['string'].str.lstrip('<strong>')
p_descs['string'] = p_descs['string'].str.rstrip(': </strong>')
p_descs['string'] = p_descs['string'].astype('string')

date = pd.DataFrame(index=pd.date_range(start = dt.datetime(2020,1,1), end = dt.datetime.now(), freq='M'))
date = date.index.to_series().apply(lambda x: dt.datetime.strftime(x, '%B %Y')).tolist()

# Cannot use length for this to determine whether it is a date or not
for l in p_descs['string']:
    p_descs['len'] = len(l.split())

for l in p_descs['string']:
    if len(l.split()) == 3:
        p_descs['date'] = 1
    else:
        p_descs['date'] = np.nan
        

    
# Date has double [[]], can we use this to differentiate it from []? I don't think we can
# get row index value if [[]] in the row

# url with NPL https://www.cnn.com/interactive/2020/us/states-reopen-coronavirus-trnd/
# stay-at-home order expired, open, reopening, 
# get text based on each id then do NLP, each div id = state, each has the same class


# Scrapping table , we just need column 1 and 3
# url https://www.nga.org/coronavirus-reopening-plans/
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

