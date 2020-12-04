import requests

# Web scrapping: reopening policy from https://www.huschblackwell.com/state-by-state-covid-19-guidance
# Note to the link we we pick a state: https://www.huschblackwell.com/illinois-state-by-state-covid-19-guidance
# state name is inserted after '/' before 'state' with '-'
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# I tried with one url first, haven't iterate over several urls
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

# Work to get paragraph with phase 4, need to get the date -> still fail since the date is also inside <p>
# Maybe use keyword to indicate that we want the date?

from datetime import datetime
p_descs['date'] = datetime.strptime(p_descs['text'],'%B %d, %Y')
p_descs['date'] = p_descs['date'].strftime('%Y-%m-%d')

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

import datetime as dt

date = pd.DataFrame(index=pd.date_range(start = dt.datetime(2020,1,1), end = dt.datetime.now(), freq='M'))
date = date.index.to_series().apply(lambda x: dt.datetime.strftime(x, '%B %Y')).tolist()

for l in p_descs['string']:
    if any(l in s for s in date):
        p_descs['date'] = 1
    else:
        p_descs['date'] = np.nan
        
p_descs['date'] = [datetime.strptime(l,'%B %d, %Y') for l in p_descs['string']]

    
# Date has double [[]], can we use this to differentiate it from []? I don't think we can
# get row index value if [[]] in the row
