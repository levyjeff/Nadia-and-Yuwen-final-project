# After checking NGA dataset, we found that many states have missing dates
# So we find another website containing better data
# Web scrapping: stay-at-home order expire date from MULTISTATE

import requests


from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
import re

head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
os.getcwd()
path_with_os = os.path.expanduser(r'~\Documents\GitHub\Nadia-and-Yuwen-final-project')


# https://docs.google.com/document/u/1/d/e/2PACX-1vSXZCFCbIRiRDRC-SWyc36T0S0hjXxT9wZAGM4V01_xtbywLBEn0o_kgmfs0dMJ4VbpPh30j2ZFZ3TH/pub
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
state_expire['expire_date'][3] = "Indefinite"  

#keep only state and expire_date
state_expire  = state_expire.drop('expire', 1)

#save to csv
state_expire.to_csv(path_or_buf = os.path.join(path_with_os, 'state_expire_multistate.csv'),  index = False)