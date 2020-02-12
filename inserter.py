import psycopg2
import pandas as pd 
from yahooScrap import YahooFinance
from suporter import num_converter

yahoo = YahooFinance('AAPL')

conn = psycopg2.connect('dbname=fin_data user=uzivatel password=postgres')


def balance_sheet():
    data = pd.DataFrame(yahoo.financials_balance())
    data.iloc[:,1:] = num_converter(data.iloc[:,1:])
    for row in data.to_numpy():
        with conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO balance_sheet (ticker, time, time_period, cash, receivables, inventory, current_assets, non_current_assets)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                ''', (yahoo.ticker[0],row[0], 'annual', row[1], row[2], row[3], row[4], row[5]))

def profile():
    data = pd.DataFrame(yahoo.profile())
    with conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO Market(industry, sector)
                VALUES(%s,%s)
                ON CONFLICT DO NOTHING
            ''', (data.loc[0,'industry'], data.loc[0,'sector']))

    with conn:
        with conn.cursor() as cur:       
            cur.execute('''
                INSERT INTO Company (ticker_id, name, address, web, contact, sector, industry, num_of_employees)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            ''', (yahoo.ticker[0], data.loc[0,'name'], data.loc[0,'address'], data.loc[0,'web'], data.loc[0,'contact'], data.loc[0,'sector'], data.loc[0,'industry'], data.loc[0,'num_of_employees'].replace(',','')))

try:
    balance_sheet()
except Exception as error:
    print(error)
else:
    print('Executed successfully')
conn.close()