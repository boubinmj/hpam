import numpy as np
import pandas as pd
from credentials_connection import User

conn = User('dev')
conn.getCredentials()
sf = conn.sf_login()

hpam = pd.read_csv('hpam.csv')

hpam['sf_id'] = ''
for index, row in hpam.iterrows():
    resp = sf.query_all("SELECT Id, Name FROM Contact WHERE NetID__c = '" + row['NetID-ALBERT'] + "'")
    try:
        hpam.at[index, 'sf_id'] = resp['records'][0]['Id']
    except:
        print("no record for " + str(row['NetID-ALBERT']))

hpam = hpam.rename(columns={'NetID-ALBERT': 'NetID__c', 'Work City': 'Work_City__c', 'Work State': 'Work_State_Province__c', 'Business Website': 'Website__c'})

print(hpam.head())