from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
import psycopg2
import urllib.parse

class YahooFinance():

    def __init__(self, ticker):
        self.ticker = ticker,
        self.url = 'https://finance.yahoo.com/quote/',
        self.balance_sheet_url = '{0}{1}/balance-sheet'.format(self.url[0], self.ticker[0]),
        self.profile_url = '{0}{1}/profile'.format(self.url[0], self.ticker[0]),
        self.statistics_url = '{0}{1}/key-statistics'.format(self.url[0], self.ticker[0]),

    def debugger(self, url):
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        IOhandler('debug.html').writer(str(response))

        return soup

    def profile(self):
        response = requests.get(self.profile_url[0]).text
        soup = BeautifulSoup(response, 'html.parser')
        
        return {
            'ticker_id': self.ticker,
            'name': soup.select('h3[data-reactid="6"]')[0].text,
            'contact': soup.select('p[data-reactid="8"] a[data-reactid="15"]')[0].extract().text,
            'web': soup.select('a[data-reactid="17"]')[0].extract().text,
            'address': soup.select('p[data-reactid="8"]')[0].text,
            'sector': soup.select('p[data-reactid="18"] span[data-reactid="21"]')[0].text,
            'industry': soup.select('p[data-reactid="18"] span[data-reactid="25"]')[0].text,
            'num_of_employees': soup.select('span[data-reactid="30"]')[0].text
        }

        

    def statistics(self):
        output = {
            'num_of_shares':'',
            'cash_per_share': '',
            'book_value_per_share':''
        }
        response = requests.get(self.statistics_url[0]).text
        soup = BeautifulSoup(response, 'html.parser')

        output['num_of_shares'] = soup.select('td[data-reactid="166"]')[0].text
        output['cash_per_share'] = soup.select('td[data-reactid="444"]')[0].text
        output['book_value_per_share'] = soup.select('td[data-reactid="472"]')[0].text

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
        response = requests.get(self.balance_sheet_url[0]).text
        soup = BeautifulSoup(response, "html.parser")

        root = "div[id='Col1-3-Financials-Proxy']"
        #dates
        output['time'].append(datetime.strptime(soup.select('span[data-reactid="34"]')[0].text, '%m/%d/%Y'))
        output['time'].append(datetime.strptime(soup.select('{0} span[data-reactid="36"]'.format(root))[0].text, '%m/%d/%Y'))
        output['time'].append(datetime.strptime(soup.select('span[data-reactid="38"]')[0].text, '%m/%d/%Y'))
        output['time'].append(datetime.strptime(soup.select('span[data-reactid="40"]')[0].text, '%m/%d/%Y'))
        #cash
        output['cash'].append(soup.select('span[data-reactid="121"]')[0].text)
        output['cash'].append(soup.select('span[data-reactid="123"]')[0].text)
        output['cash'].append(soup.select('span[data-reactid="125"]')[0].text)
        output['cash'].append(soup.select('span[data-reactid="127"]')[0].text)
        #receivables
        output['receivables'].append(soup.select('span[data-reactid="136"]')[0].text)
        output['receivables'].append(soup.select('span[data-reactid="138"]')[0].text)
        output['receivables'].append(soup.select('span[data-reactid="140"]')[0].text)
        output['receivables'].append(soup.select('span[data-reactid="142"]')[0].text)
        #inventory
        output['inventory'].append(soup.select('span[data-reactid="151"]')[0].text)
        output['inventory'].append(soup.select('span[data-reactid="153"]')[0].text)
        output['inventory'].append(soup.select('span[data-reactid="155"]')[0].text)
        output['inventory'].append(soup.select('span[data-reactid="157"]')[0].text)
        #current_assets
        output['current_assets'].append(soup.select('span[data-reactid="181"]')[0].text)
        output['current_assets'].append(soup.select('span[data-reactid="183"]')[0].text)
        output['current_assets'].append(soup.select('span[data-reactid="185"]')[0].text)
        output['current_assets'].append(soup.select('span[data-reactid="187"]')[0].text)
        #non_current_assets
        output['non_current_assets'].append(soup.select('span[data-reactid="325"]')[0].text)
        output['non_current_assets'].append(soup.select('span[data-reactid="327"]')[0].text)
        output['non_current_assets'].append(soup.select('span[data-reactid="329"]')[0].text)
        output['non_current_assets'].append(soup.select('span[data-reactid="331"]')[0].text)

        return output

# yahoo = YahooFinance('AAPL')
# yahoo.financials_balance()

class IOhandler():
    def __init__(self, file):
        self.file = file

    def writer(self, text):
        f = open(self.file, 'w')
        f.write(str(text))
        f.close()

#fileHandler = IOhandler('test.html')

#fileHandler.writer(yahoo.financials_balance('https://finance.yahoo.com/quote/AAPL/balance-sheet?p=AAPL'))
YahooFinance('AAPL').debugger('https://finance.yahoo.com/quote/AAPL/profile')
#appl = yf.Ticker('APPL')
#response = requests.get('')

#fileHandler.writer(str(response.headers))

