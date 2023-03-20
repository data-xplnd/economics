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

url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?page[number]=1"



response = requests.request("GET", url).json()

count=response['meta']['total-count']

url = f"https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?page[number]=1&page[size]={count}"

response = requests.request("GET", url).json()


data=pd.DataFrame(response['data'])

add_table(data,'treasury_securities')
