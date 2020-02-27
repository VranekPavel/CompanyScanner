import psycopg2
import pandas as pd 
from yFin import YF
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine('postgresql://uzivatel:postgres@localhost:5432/fin_data')

def company(data):
    pd.DataFrame(data.company, index=[0]).to_sql('company', con=engine, if_exists='append', index=False, schema='public')

def market(data):
    pd.DataFrame(data.market, index=[0]).to_sql('market', con=engine, if_exists='append', index=False, schema='public')

def stock(data):
    pd.DataFrame(data.stock, index=[0]).to_sql('stock', con=engine, if_exists='append', index=False, schema='public')

def statistics(data):
    pd.DataFrame(data.statistics, index=[0]).to_sql('statistics', con=engine, if_exists='append', index=False, schema='public')

def dividends(data):
    data.dividends().to_sql('dividends', con=engine, if_exists='append', index=False, schema='public')

def financials(data):
    data.financials().to_sql('financials', con=engine, if_exists='append', index=False, schema='public')

def stock_holders(data):
    data.stock_holders().to_sql('stock_holders', con=engine, if_exists='append', index=False, schema='public')

def balance_sheet(data):
    data.balance_sheet().to_sql('balance_sheet', con=engine, if_exists='append', index=False, schema='public')

def cash_flow(data):
    data.cashFlow().to_sql('cash_flow', con=engine, if_exists='append', index=False, schema='public')

def earnings(data):
    data.earnings().to_sql('earnings', con=engine, if_exists='append', index=False, schema='public')

def sustainability(data):
    data.sustainability().to_sql('sustainability', con=engine, if_exists='append', index=False, schema='public')

def recommendations(data):
    data.recommendations().to_sql('recommendations', con=engine, if_exists='append', index=False, schema='public')

class IOhandler():
    def __init__(self, file):
        self.file = file

    def write(self, text):
        f = open(self.file, 'a')
        f.write(str(text))
        f.close()

def insertTicker():
    data = YF('AAPL')
    error_log = IOhandler('error_log.txt')
    log = IOhandler('log.txt')
    funcs = [company, market, stock, statistics, dividends, financials, stock_holders, balance_sheet, cash_flow, earnings, sustainability, recommendations]
    err = 0
    for func in funcs:
        try:
            func(data)
        except Exception as error:
            if type(error).__name__ == 'IntegrityError':
                log.write('{}({}): already in database\n'.format(data.ticker[0], datetime.now().isoformat(timespec='minutes')))
                print('{}: already in database'.format(data.ticker[0]))
                break
            else:
                err += 1
                print(type(error).__name__)
                error_log.write('{}, Ticker: {}, Func: {},  Error: {}\n'.format(datetime.now().isoformat(timespec='minutes') ,data.ticker[0] , func, error))
            continue
        else:
            print('{}: success'. format(func))
    else:
        log.write('{}({}): job done with {} error(s)\n'.format(data.ticker[0], datetime.now().isoformat(timespec='minutes'), err))
        print('{}: job done with {} error(s)'.format(data.ticker[0], err))

insertTicker()