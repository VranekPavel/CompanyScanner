from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
import psycopg2

class SoupExtractor():
    def __init__(self, url):
        self.response = requests.get(url).text
        self.soup = BeautifulSoup(self.response, 'html.parser')

    def extract(self, css):
        if self.soup.select(css):
           return self.soup.select(css)[0].extract().text
        else:
            return '' 


class YahooFinance():

    def __init__(self, ticker):
        self.ticker = ticker,
        self.url = 'https://finance.yahoo.com/quote/',
        self.balance_sheet_url = '{0}{1}/balance-sheet'.format(self.url[0], self.ticker[0]),
        self.profile_url = '{0}{1}/profile'.format(self.url[0], self.ticker[0]),
        self.statistics_url = '{0}{1}/key-statistics'.format(self.url[0], self.ticker[0]),

    def debugger(self, url):
        print(url)
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        IOhandler('debug.html').writer(str(response))

        return soup

    def profile(self):
        soupEx = SoupExtractor(self.profile_url[0])

        return {
                'ticker_id': self.ticker,
                'name': soupEx.extract('h3[data-reactid="6"]'),
                'contact': soupEx.extract('p[data-reactid="8"] a[data-reactid="15"]'),
                'web': soupEx.extract('a[data-reactid="17"]'),
                'address': soupEx.extract('p[data-reactid="8"]'),
                'sector': soupEx.extract('p[data-reactid="18"] span[data-reactid="21"]'),
                'industry': soupEx.extract('p[data-reactid="18"] span[data-reactid="25"]'),
                'num_of_employees': soupEx.extract('span[data-reactid="30"]')
        } 

    def statistics(self):
        output = {
            'num_of_shares':'',
            'cash_per_share': '',
            'book_value_per_share':''
        }
        soupEx = SoupExtractor(self.statistics_url[0])

        output['num_of_shares'] = soupEx.extract('td[data-reactid="166"]')
        output['cash_per_share'] = soupEx.extract('td[data-reactid="444"]')
        output['book_value_per_share'] = soupEx.extract('td[data-reactid="472"]')

        return output

    def financials_balance(self):
        output = {
            'time':[],
            'cash':[],
            'receivables':[],
            'inventory':[],
            'current_assets':[],
            'non_current_assets':[]
        
        }
        soupEx = SoupExtractor(self.balance_sheet_url[0])

        root = "div[id='Col1-3-Financials-Proxy']"
        #dates
        output['time'].append(soupEx.extract('span[data-reactid="34"]'))
        output['time'].append(soupEx.extract('{0} span[data-reactid="36"]'.format(root)))
        output['time'].append(soupEx.extract('span[data-reactid="38"]'))
        output['time'].append(soupEx.extract('span[data-reactid="40"]'))
        #cash
        output['cash'].append(soupEx.extract('span[data-reactid="117"]'))
        output['cash'].append(soupEx.extract('span[data-reactid="119"]'))
        output['cash'].append(soupEx.extract('span[data-reactid="121"]'))
        output['cash'].append(soupEx.extract('span[data-reactid="123"]'))
        #receivables
        output['receivables'].append(soupEx.extract('span[data-reactid="132"]'))
        output['receivables'].append(soupEx.extract('span[data-reactid="134"]'))
        output['receivables'].append(soupEx.extract('span[data-reactid="136"]'))
        output['receivables'].append(soupEx.extract('span[data-reactid="138"]'))
        #inventory
        output['inventory'].append(soupEx.extract('span[data-reactid="147"]'))
        output['inventory'].append(soupEx.extract('span[data-reactid="149"]'))
        output['inventory'].append(soupEx.extract('span[data-reactid="151"]'))
        output['inventory'].append(soupEx.extract('span[data-reactid="153"]'))
        #current_assets
        output['current_assets'].append(soupEx.extract('span[data-reactid="175"]'))
        output['current_assets'].append(soupEx.extract('span[data-reactid="177"]'))
        output['current_assets'].append(soupEx.extract('span[data-reactid="179"]'))
        output['current_assets'].append(soupEx.extract('span[data-reactid="181"]'))
        #non_current_assets
        output['non_current_assets'].append(soupEx.extract('span[data-reactid="315"]'))
        output['non_current_assets'].append(soupEx.extract('span[data-reactid="317"]'))
        output['non_current_assets'].append(soupEx.extract('span[data-reactid="319"]'))
        output['non_current_assets'].append(soupEx.extract('span[data-reactid="321"]'))

        return output

# yahoo = YahooFinance('TSLA')
# print(yahoo.profile())



class IOhandler():
    def __init__(self, file):
        self.file = file

    def writer(self, text):
        f = open(self.file, 'w')
        f.write(str(text))
        f.close()

#fileHandler = IOhandler('test.html')

#fileHandler.writer(yahoo.financials_balance('https://finance.yahoo.com/quote/AAPL/balance-sheet?p=AAPL'))
#YahooFinance('TNET').debugger('https://finance.yahoo.com/quote/TNET/balance-sheet')
#appl = yf.Ticker('APPL')
#response = requests.get('')

#fileHandler.writer(str(response.headers))

