import os
import requests
import pandas as pd

# Download the data from https://api.covidtracking.com
path = os.path.abspath(os.path.dirname(__file__))
url = r'https://api.covidtracking.com/v1/states/daily.csv'

def get_statement(url, fname, path):
    response = requests.get(url)
    assert(fname.endswith('.csv')), 'Incorrect file type in get_statement, expected csv, got: {}'.format(url)
    with open(os.path.join(path, fname), 'wb') as file:
        file.write(response.content)

go_online = False # Change True if the file(s) not yet in the folder (see files)
fname = [] 
fname = url.split('/')[-1]
if go_online:
    get_statement(url, fname, path)

files = [file for file in os.listdir(path) if file.endswith('csv')]
df = pd.read_csv(files[0])

# Web scrapping: reopening policy from https://www.huschblackwell.com/state-by-state-covid-19-guidance
# Note to the link we we pick a state: https://www.huschblackwell.com/illinois-state-by-state-covid-19-guidance
# state name is inserted after '/' before 'state' with '-'
import requests
from bs4 import BeautifulSoup

urls = []
url = r'https://www.huschblackwell.com/illinois-state-by-state-covid-19-guidance'
head = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

resp = requests.get(url, headers=head)
soup = BeautifulSoup(resp.text, 'html.parser')

# <div class web content
# use <strong>, under <p>

# reopen may be within li or p
idx = [] # I define a function to get a list of index location of element that contains certain string
def indices(self):
    for i, elem in enumerate(self): #https://stackoverflow.com/questions/5466618/too-many-values-to-unpack-iterating-over-a-dict-key-string-value-list
        if 'reopen' in elem.text:
            idx.append(i)
        elif 'reopening' in elem.text:
            idx.append(i)
    return idx

idx_li = indices(soup.find_all('li'))
idx_p = indices(soup.find_all('p'))

lis = soup.find_all('li')[idx_li]

