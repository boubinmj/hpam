import numpy as np
import pandas as pd
from credentials_connection import User
from thefuzz import fuzz
from thefuzz import process
import requests
import json

def conn_sf():
    conn = User('dev')
    conn.getCredentials()
    sf = conn.sf_login()
    return sf

def update_field(sf, field, df):
    for index, row in df[df[field] != ''].iterrows():
        sf.Contact.update(row['sf_id'], {field: str(row[field])})


hp = pd.read_csv('with_employers.csv')
for el in hp.columns:
    print(el)

sf = conn_sf()

for index, row in hp[~hp['AccountId'].isna()].iterrows():
    print(row['AccountId'])
    try:
        sf.Contact.update(row['sf_id'], {'AccountId': str(row['AccountId'])})
    except:
        print(row['NetID__c'])