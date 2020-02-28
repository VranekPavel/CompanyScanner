
from inserter import insertTicker
from yahooScrap import YahooFinanceTickers
url = input('Input url:')

tickers = YahooFinanceTickers(url).tickers()

print('Url returned {} ticker(s)'.format(len(tickers)))
print('Starting to insert values into database')
for ticker in tickers:
    try:
        print(insertTicker(ticker))
    except Exception as error:
        print('Ticker: {}, Error: {}'.format(ticker, error))
        input('Press enter for next ticker')
input()