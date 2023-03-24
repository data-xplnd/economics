import pandas as pd
import requests
import os
from sqlalchemy import create_engine
from urllib.parse import quote
from io import StringIO
from creds import pw
from creds import db

def add_table(df,table):

    # script to create sql database for needed tables
    engine = create_engine(f'mysql+pymysql://admin:{pw}@{db}')
    df.to_sql(f"{table}",con=engine, if_exists='replace')


year =1990

dfs=[]

while year < 2024:

    print(year)


    url=f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value={year}"

    df=pd.read_html(url)

    df2=df[0].drop(df[0].columns[[ 1, 2]], axis=1)
    dfs.append(df2)

    year+=1

# print(dfs)

data_concat = pd.concat(dfs,             
                      ignore_index = True,
                      sort = False)


data_concat.to_csv("economics/outputs/par_yield_rates.csv")

add_table(data_concat,'par_yield_rates')

print('par_yield_rates table added to db')