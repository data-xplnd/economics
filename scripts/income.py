import pandas as pd
import requests
import os
from sqlalchemy import create_engine
from urllib.parse import quote
from io import StringIO
from creds import pw
from creds import db

# function to add table to db
def add_table(df,table):

    # script to create sql database for needed tables
    engine = create_engine(f'mysql+pymysql://admin:{pw}@{db}')
    df.to_sql(f"{table}",con=engine, if_exists='replace')

# the csv comes from and is to be updated monthly:
# https://apps.bea.gov/iTable/?reqid=19&step=2&isuri=1&categories=survey#eyJhcHBpZCI6MTksInN0ZXBzIjpbMSwyLDNdLCJkYXRhIjpbWyJjYXRlZ29yaWVzIiwiU3VydmV5Il0sWyJOSVBBX1RhYmxlX0xpc3QiLCI2NSJdXX0=
df=pd.read_csv('economics/inputs/personal_income.csv')

add_table(df,'income')

print('income table added to db')
