def model(dbt,session):
    import pandas as pd
    import requests
    import os
    from sqlalchemy import create_engine
    from urllib.parse import quote
    from io import StringIO

    # url and content for BLS CPI data
    url='https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CPIAUCSL,CPIFABSL,CUSR0000SAF115,CUSR0000SEFR,CUSR0000SEFS,CUSR0000SEFT,CUSR0000SEFV,CUSR0000SEFV05,CUSR0000SAF116,CUSR0000SEFW,CUSR0000SEFX,CPIHOSSL&scale=left,left,left,left,left,left,left,left,left,left,left,left&cosd=1947-01-01,1967-01-01,1967-01-01,1989-01-01,1989-01-01,1981-01-01,1953-01-01,1998-01-01,1967-01-01,1978-01-01,1978-01-01,1967-01-01&coed=2023-02-01,2023-02-01,2023-02-01,2023-02-01,2023-02-01,2023-02-01,2023-02-01,2023-02-01,2023-02-01,2023-02-01,2023-02-01,2023-02-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92,%2391e8e1,%238d4653,%238085e8&link_values=false,false,false,false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9,10,11,12&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19&revision_date=2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19,2023-03-19&nd=1947-01-01,1967-01-01,1967-01-01,1989-01-01,1989-01-01,1981-01-01,1953-01-01,1998-01-01,1967-01-01,1978-01-01,1978-01-01,1967-01-01'

    req=requests.get(url)
        
    url_content=req.content
    # print(url_content)

    s=str(url_content,'utf-8')

    data = StringIO(s) 

    data_df=pd.read_csv(data)

    # add_table(data_df,"cpi")

    # print("CPI data added to db")

    # core_cpi_url='https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CPILFESL&scale=left&cosd=1957-01-01&coed=2023-02-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2023-03-19&revision_date=2023-03-19&nd=1957-01-01'

    # req=requests.get(core_cpi_url)
        
    # url_content=req.content
    # # print(url_content)

    # s=str(url_content,'utf-8')

    # data = StringIO(s) 

    # df=pd.read_csv(data)

    # add_table(df,"core_cpi")

    # print("Core CPI data added to db")

    # # map the code to the names of the metrics and add the dataframe to database

    labels=[
        {'name':'All Items in U.S. City Average',
        'code': 'CPIAUCSL'},
        {'name':'Food and Beverages in U.S. City Average',
        'code': 'CPIFABSL'},
        {'name':'Other Food at Home in U.S. City Average',
        'code': 'CUSR0000SAF115'},
        {'name':'Sugar and Sweets in U.S. City Averagee',
        'code': 'CUSR0000SEFR'},
        {'name':'Fats and Oils in U.S. City Average ',
        'code': 'CUSR0000SEFS'},
        {'name':'Other Foods in U.S. City Average',
        'code': 'CUSR0000SEFT'},
        {'name':'Food Away from Home in U.S. City Average',
        'code': 'CUSR0000SEFV'},
        {'name':'Other Food Away from Home in U.S. City Average',
        'code': 'CUSR0000SEFV05'},
        {'name':'Alcoholic Beverages in U.S. City Average',
        'code': 'CUSR0000SAF116'},
        {'name':'Alcoholic Beverages at Home in U.S. City Average',
        'code': 'CUSR0000SEFW'},
        {'name':'Alcoholic Beverages Away from Home in U.S. City Average',
        'code': 'CUSR0000SEFX'},
        {'name':'Housing in U.S. City Average',
        'code': 'CPIHOSSL'},
        {'name':'All Items Less Food and Energy in U.S. City Average',
        'code': 'CPILFESL'}
    ]

    # cpi_labels=pd.DataFrame(labels)

    # add_table(cpi_labels,"cpi_labels")

    print("CPI labels table added to db")

    return data_df