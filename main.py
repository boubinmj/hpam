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

def add_sf_Contact_ids(sf, df, field_name):
    df['sf_id'] = ''
    for index, row in df.iterrows():
        try:
            resp = sf.query_all("SELECT Id FROM Contact WHERE NetID__c = '" + row[field_name] + "'")['records']
            df.at[index, 'sf_id'] = resp[0]['Id']
        except Exception as e:
            print(e)
            print("No record for NetID: " + str(row[field_name]))
    
    print("Total Profiles: " + str(len(df)))
    print("Total SF Records: " + str(len(df[df['sf_id'] != ''])))
    print("Total Profiles with Employment: " + str(len(df[df['field_employer'] != ''])))

    return df

def get_sf_accounts(sf):
    acc = pd.DataFrame(sf.query_all("SELECT Id, Name FROM Account")['records'])
    acc.to_csv("accounts.csv")

def search_Employers(sf, df, field):
    df['AccountId'] = ''
    acc = pd.read_csv('accounts.csv')
    for idx, record in df[df[field] != ''].iterrows():
        print("### " + str(record[field]) + " ###\n\n")
        for index, row in acc.iterrows():
            if(fuzz.ratio(row['Name'], record[field])>90):
                print(row['Id'] + " " + row['Name'])
                df.at[idx, 'AccountId'] = row['Id']
    return df

sf = conn_sf()

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
get_sf_accounts(sf)
hpam = search_Employers(sf, hpam, 'Employer')

print(hpam.head())
hpam.to_csv('with_employers.csv')