import os
import requests
import pandas as pd

# Download the data from https://api.covidtracking.com
path = os.path.abspath(os.path.dirname(__file__))
api = r'https://api.covidtracking.com/v1/states/daily.csv'

def get_statement(api, fname, path):
    response = requests.get(url)
    assert(fname.endswith('.csv')), 'Incorrect file type in get_statement, expected csv, got: {}'.format(url)
    with open(os.path.join(path, fname), 'wb') as file:
        file.write(response.content)

go_online = False # Change True if the file(s) not yet in the folder (see files)
fname = [] 
fname = api.split('/')[-1]
if go_online:
    get_statement(api, fname, path)

files = [file for file in os.listdir(path) if file.endswith('csv')]
df = pd.read_csv(files[0])

# Web scrapping: reopening policy from https://www.huschblackwell.com/state-by-state-covid-19-guidance
# Note to the link we we pick a state: https://www.huschblackwell.com/illinois-state-by-state-covid-19-guidance
# state name is inserted after '/' before 'state' with '-'
from bs4 import BeautifulSoup

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
p_phase4 = []
for i in idx_p:
    p_phase4.append(p_descs[i-1])

# We might need to do NPL to get that the state moves into phase 4?