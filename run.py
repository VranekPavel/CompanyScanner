from inserter import insertTicker, IOhandler
from yahooScrap import YahooFinanceTickers
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


error_log = IOhandler('run_error_log.txt')
database = pd.read_csv('data.csv')
database = database['ticker_id'].values
# new_ticks = pd.read_csv('../../inputs/tickers/LSE.txt', sep='\t')

def insert_tickers(tickers):
    print('{} tickers'.format(len(tickers)))
    success = 0
    i = 1
    for ticker in tickers:
        if ticker not in database:
            try:
                insertTicker(ticker)
                success += 1
            except Exception as error:
                error_log.write('\n{} ,Ticker: {}, Error: {}'.format(datetime.now().isoformat(timespec='minutes'), ticker, error))
        printProgressBar(i, len(tickers))
        i += 1    

    print('{} from {} Tickers was inserted into database'.format(success, len(tickers)))

print('How will you insert tickers:')
print('URL: 0')
print('File: 1')
print('Ticker: 2')
input_type = input('Choosen option:')
if int(input_type) == 0:
    url = input('Input url:')
    tickers = YahooFinanceTickers(url).tickers()
elif int(input_type) == 2:
    ticker = input('Input ticker:')
    insert_tickers([ticker])
else:
    file = input('Input file name:')
    tickers = pd.read_csv('../../inputs/tickers/{}'.format(file), sep='\t')
    insert_tickers(tickers['Symbol'])

# for i in range(0, 61500, 100):
#     print('{} of 611'.format(i / 100))
#     tickers = YahooFinanceTickers('https://finance.yahoo.com/screener/unsaved/e68a0a09-cde0-438a-98cb-86b1a1377e73?offset={}&count=100'.format(i)).tickers()
#     insert_tickers(tickers)