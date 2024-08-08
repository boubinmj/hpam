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

sf = conn_sf()

df = pd.DataFrame(sf.query_all("SELECT LastModifiedDate FROM Account LIMIT 200")['records'])

for index, row in df.iterrows():
    print(row['LastModifiedDate'])
