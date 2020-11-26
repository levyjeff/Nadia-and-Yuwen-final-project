# This is the script for python project

import os
import requests
import pandas as pd

# Download the data from https://api.covidtracking.com
path = os.path.abspath(os.path.dirname(__file__))
url = r'https://api.covidtracking.com/v1/states/daily.csv'

def get_statement(url, fname, path):
    response = requests.get(url)
    assert(fname.endswith('.csv')), 'Incorrect file type in get_statement, expected PDF, got: {}'.format(url)
    with open(os.path.join(path, fname), 'wb') as file:
        file.write(response.content)

go_online = False # Change True if the file(s) not yet in the folder (see files)
fname = [] 
fname = url.split('/')[-1]
if go_online:
    get_statement(url, fname, path)

files = [file for file in os.listdir(path) if file.endswith('csv')]
df = pd.read_csv(files[0])