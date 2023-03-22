import requests
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote
from io import StringIO
from creds import pw
from creds import db



def add_table(df,table):

    # script to create sql database for needed tables
    engine = create_engine(f'mysql+pymysql://admin:{pw}@{db}')
    df.to_sql(f"{table}",con=engine, if_exists='replace')
    
eps=['1','2','3','4','5','6','6a','6b','6c','6d','6e','7','8','9']
dfs=[]

for ep in eps:
    
    url = f"https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_{ep}"

    response = requests.request("GET", url).json()

    count=response['meta']['total-count']
    print(ep)
    print(count)

    url = f"https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_{ep}"

    response = requests.request("GET", url).json()
    
    # print(response)


    data=pd.DataFrame(response['data'])
    
    dfs.append(data)

print(dfs)

data_concat = pd.concat(dfs,             
                      ignore_index = True,
                      sort = False)


data_concat.to_csv("economics/outputs/monthly_treasury.csv")

add_table(data_concat,'monthly_treasury')

print('added monthly treasury statements to db')
