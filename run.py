
from inserter import insertTicker
from yahooScrap import YahooFinanceTickers
import yfinance as yf
url = input('Input url:')

tickers = YahooFinanceTickers(url).tickers()

print('Url returned {} ticker(s)'.format(len(tickers)))
print('Starting to insert values into database')
err = 0
i = 1
for ticker in tickers:
    try:
        print(insertTicker(ticker))
    except Exception as error:
        err += 1
        print('Ticker: {}, Error: {}'.format(ticker, error))
    print('{}% done'.format(i))
    i += 1
print('{} from 100 Tickers was inserted into database'.format(100-err))
input()