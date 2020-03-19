
from inserter import insertTicker, IOhandler
from yahooScrap import YahooFinanceTickers
import yfinance as yf

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

url = input('Input url:')
tickers = YahooFinanceTickers(url).tickers()
error_log = IOhandler('error_log.txt')

print('Url returned {} ticker(s)'.format(len(tickers)))
err = 0
i = 1
for ticker in tickers:
    try:
        insertTicker(ticker)
    except Exception as error:
        err += 1
        error_log.write('\nTicker: {}, Error: {}'.format(ticker, error))
    printProgressBar(i, len(tickers))
    i += 1
print('{} from {} Tickers was inserted into database'.format(len(tickers)-err, len(tickers)))
