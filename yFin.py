
from yfinance_master import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import re

#data[0] = yf.Ticker('AAPL')
class YF():
    def __init__(self, ticker):
        self.ticker = ticker,
        self.data = yf.Ticker(self.ticker[0]),
        self.market = {
            'ticker_id':self.data[0].info['symbol'],
            'sector': self.data[0].info['sector'],
            'industry': self.data[0].info['industry']
        },
        self.stock ={
            'ticker_id': self.data[0].info['symbol'],
            'currency': self.data[0].info['currency'],
            'exchange': self.data[0].info['exchange'],
            'exchangeTimezoneName': self.data[0].info['exchangeTimezoneName'],
            'exchangeTimezoneShortName': self.data[0].info['exchangeTimezoneShortName'],
            'open': self.data[0].info['open'],
            'bid': self.data[0].info['bid'],
            'bidSize': self.data[0].info['bidSize'],
            'dayHigh': self.data[0].info['dayHigh'],
            'dayLow': self.data[0].info['dayLow'],
            'ask': self.data[0].info['ask'],
            'askSize': self.data[0].info['askSize'],
            'previousClose': self.data[0].info['previousClose'],
            'regularMarketOpen': self.data[0].info['regularMarketOpen'],
            'regularMarketPrice': self.data[0].info['regularMarketPrice'],
            'regularMarketPreviousClose': self.data[0].info['regularMarketPreviousClose'],
            'regularMarketDayHigh': self.data[0].info['regularMarketDayHigh'],
            'regularMarketDayLow': self.data[0].info['regularMarketDayLow'],
            'regularMarketVolume': self.data[0].info['regularMarketVolume'],
            'volume': self.data[0].info['volume'],
            'averageVolume': self.data[0].info['averageVolume'],
            'averageDailyVolume10Day': self.data[0].info['averageDailyVolume10Day'],
            'averageVolume10days': self.data[0].info['averageVolume10days'],
            'fiftyTwoWeekHigh': self.data[0].info['fiftyTwoWeekHigh'],
            'fiftyTwoWeekLow': self.data[0].info['fiftyTwoWeekLow'],
            'fiftyTwoWeekChange': self.data[0].info['52WeekChange'],
            'fiftyDayAverage': self.data[0].info['fiftyDayAverage'],
            'twoHundredDayAverage': self.data[0].info['twoHundredDayAverage'],
            'ytdReturn': self.data[0].info['ytdReturn'],
            'sharesOutstanding': self.data[0].info['sharesOutstanding'],
            'sharesPercentSharesOut': self.data[0].info['sharesPercentSharesOut'],
            'SandP52WeekChange': self.data[0].info['SandP52WeekChange'],
            'sharesShort': self.data[0].info['sharesShort'],
            'sharesShortPreviousMonthDate': self.data[0].info['sharesShortPreviousMonthDate'],
            'sharesShortPriorMonth': self.data[0].info['sharesShortPriorMonth'],
            'floatShares': self.data[0].info['floatShares'],
            'lastSplitDate': self.data[0].info['lastSplitDate'],
            'lastSplitFactor': self.data[0].info['lastSplitFactor'],
            'trailingAnnualDividendYield': self.data[0].info['trailingAnnualDividendYield'],
            'trailingAnnualDividendRate': self.data[0].info['trailingAnnualDividendRate'],
            'yield': self.data[0].info['yield'],
            'fiveYearAvgDividendYield': self.data[0].info['fiveYearAvgDividendYield'],
            'dividendYield': self.data[0].info['dividendYield'],
            'dividendRate': self.data[0].info['dividendRate'],
            'exDividendDate': self.data[0].info['exDividendDate'],
        },
        self.statistics = {
            'ticker_id': self.data[0].info['symbol'],
            'payoutRatio': self.data[0].info['payoutRatio'],
            'beta': self.data[0].info['beta'],
            'beta3Year': self.data[0].info['beta3Year'],
            'trailingPE': self.data[0].info['trailingPE'],
            'forwardPE': self.data[0].info['forwardPE'],
            'priceToSalesTrailing12Months': self.data[0].info['priceToSalesTrailing12Months'],
            'enterpriseToRevenue': self.data[0].info['enterpriseToRevenue'],
            'profitMargins': self.data[0].info['profitMargins'],
            'enterpriseToEbitda': self.data[0].info['enterpriseToEbitda'],
            'forwardEps': self.data[0].info['forwardEps'],
            'heldPercentInstitutions': self.data[0].info['heldPercentInstitutions'],
            'netIncomeToCommon': self.data[0].info['netIncomeToCommon'],
            'trailingEps': self.data[0].info['trailingEps'],
            'priceToBook': self.data[0].info['priceToBook'],
            'heldPercentInsiders': self.data[0].info['heldPercentInsiders'],
            'shortRatio': self.data[0].info['shortRatio'],
            'threeYearAverageReturn': self.data[0].info['threeYearAverageReturn'],
            'earningsQuarterlyGrowth': self.data[0].info['earningsQuarterlyGrowth'],
            'revenueQuarterlyGrowth': self.data[0].info['revenueQuarterlyGrowth'],
            'pegRatio': self.data[0].info['pegRatio'],
            'lastCapGain': self.data[0].info['lastCapGain'],
            'shortPercentOfFloat': self.data[0].info['shortPercentOfFloat'],
            'fiveYearAverageReturn': self.data[0].info['fiveYearAverageReturn'],
            'bookValue': self.data[0].info['bookValue'],
            'marketCap': self.data[0].info['marketCap'],
            'enterpriseValue': self.data[0].info['enterpriseValue'],
            'annualHoldingsTurnover': self.data[0].info['annualHoldingsTurnover'],
            'totalAssets': self.data[0].info['totalAssets'], 
            'circulatingSupply': self.data[0].info['circulatingSupply']
        },
        self.company = {
            'ticker_id': self.data[0].info['symbol'],
            'shortName': self.data[0].info['shortName'],
            'longName': self.data[0].info['longName'], 
            'zip': self.data[0].info['zip'],
            'fullTimeEmployees': self.data[0].info['fullTimeEmployees'],
            'longBusinessSummary': self.data[0].info['longBusinessSummary'],
            'city': self.data[0].info['city'],
            'phone': self.data[0].info['phone'],
            'state': self.data[0].info['state'],
            'country': self.data[0].info['country'],
            'website': self.data[0].info['website'],
            'address': self.data[0].info['address1'],
            'isEsgPopulated': self.data[0].info['isEsgPopulated'],
            'quoteType': self.data[0].info['quoteType'],
            'market': self.data[0].info['market'],
            'morningStarRiskRating': self.data[0].info['morningStarRiskRating'],
            'fundFamily': self.data[0].info['fundFamily'],
            'lastFiscalYearEnd': self.data[0].info['lastFiscalYearEnd'],
            'nextFiscalYearEnd': self.data[0].info['nextFiscalYearEnd'],
            'mostRecentQuarter': self.data[0].info['mostRecentQuarter'],
            'legalType': self.data[0].info['legalType'],
            'morningStarOverallRating': self.data[0].info['morningStarOverallRating'],
        }
    
    def dividends(self):
        dividends = pd.DataFrame(self.data[0].dividends)
        dividends = dividends.reset_index()
        dividends['ticker_id'] = self.ticker[0]
        dividends.columns = ['time', 'value', 'ticker_id']
        return dividends

    def financials(self):
        financials = self.data[0].financials.swapaxes('index', 'columns').reset_index()
        financials['ticker_id'] = self.ticker[0]
        financials['timePeriod'] = 'anual'
        quarter_financials = self.data[0].quarterly_financials.swapaxes('index', 'columns').reset_index()
        quarter_financials['ticker_id'] = self.ticker[0]
        quarter_financials['timePeriod'] = 'quarter'
        fin = financials.append(quarter_financials)
        fin.columns = ['time', 'researchDevelopment', 'accountingCharges',
       'incomeBeforeTax', 'minorityInterest', 'netIncome',
       'sellingGeneralAdministrative', 'grossProfit', 'ebit',
       'operatingIncome', 'otherOperatingExpenses', 'interestExpense',
       'extraordinaryItems', 'nonRecurring', 'otherItems',
       'incomeTaxExpense', 'totalRevenue', 'totalOperatingExpenses',
       'costOfRevenue', 'totalOtherIncomeExpenseNet',
       'discontinuedOperations', 'netIncomeFromContinuingOps',
       'netIncomeApplicableToCommonShares', 'ticker_id', 'timePeriod']
        return fin
    
    def stock_holders(self):
        stock_holders = pd.DataFrame(self.data[0].major_holders[0]).swapaxes('index', 'columns')
        stock_holders.columns = ['insiders', 'institutions', 'institutions_float', 'numOfInstitutions']
        stock_holders['ticker_id'] = self.ticker[0]
        return stock_holders

    def balance_sheet(self):
        balance_sheet = self.data[0].balance_sheet.swapaxes('index', 'columns').reset_index()
        balance_sheet['ticker_id'] = self.ticker[0]
        balance_sheet['timePeriod'] = 'anual'
        quarter_balance_sheet = self.data[0].quarterly_balance_sheet.swapaxes('index', 'columns').reset_index()
        quarter_balance_sheet['ticker_id'] = self.ticker[0]
        quarter_balance_sheet['timePeriod'] = 'quarter'
        balance = balance_sheet.append(quarter_balance_sheet)
        balance.rename(columns={'':'time'},inplace=True)
        balance = balance[['time', 'Total Liab', 'Total Stockholder Equity', 'Other Current Liab',
        'Total Assets', 'Common Stock', 'Other Current Assets',
        'Retained Earnings', 'Other Liab', 'Treasury Stock', 'Other Assets',
        'Cash', 'Total Current Liabilities', 'Short Long Term Debt',
        'Other Stockholder Equity', 'Property Plant Equipment',
        'Total Current Assets', 'Long Term Investments', 'Net Tangible Assets',
        'Short Term Investments', 'Net Receivables', 'Long Term Debt',
        'Inventory', 'Accounts Payable', 'Intangible Assets', 'Good Will',
        'ticker_id', 'timePeriod']]
        balance.columns = self.normalize(balance.columns)
        return balance

    def cashFlow(self):
        cashFlow = self.data[0].cashflow.swapaxes('index', 'columns').reset_index()
        cashFlow['ticker_id'] = self.ticker[0]
        cashFlow['timePeriod'] = 'anual'
        quarter_cashFlow = self.data[0].quarterly_cashflow.swapaxes('index', 'columns').reset_index()
        quarter_cashFlow['ticker_id'] = self.ticker[0]
        quarter_cashFlow['timePeriod'] = 'quarter'
        cash = cashFlow.append(quarter_cashFlow)
        cash.rename(columns={'':'time'},inplace=True)
        cash = cash[['time', 'Investments', 'Change To Liabilities',
        'Total Cashflows From Investing Activities', 'Net Borrowings',
        'Total Cash From Financing Activities',
        'Change To Operating Activities', 'Issuance Of Stock', 'Net Income',
        'Change In Cash', 'Repurchase Of Stock',
        'Total Cash From Operating Activities', 'Depreciation',
        'Other Cashflows From Investing Activities', 'Dividends Paid',
        'Change To Inventory', 'Change To Account Receivables',
        'Other Cashflows From Financing Activities', 'Change To Netincome',
        'Capital Expenditures', 'ticker_id', 'timePeriod']]
        cash.columns = self.normalize(cash.columns)
        return cash

    def earnings(self):
        earnings = self.data[0].earnings.reset_index()
        earnings['ticker_id'] = self.ticker[0]
        earnings['timePeriod'] = 'anual'
        quarter_earnings = self.data[0].quarterly_earnings.reset_index()
        quarter_earnings.columns = ['Year', 'Revenue', 'Earnings']
        quarter_earnings['ticker_id'] = self.ticker[0]
        quarter_earnings['timePeriod'] = 'quarter'
        return earnings.append(quarter_earnings)

    def sustainability(self):
        sustainability = self.data[0].sustainability.swapaxes('index', 'columns')
        columns = sustainability.columns
        columns = columns.insert(0, 'ticker_id')
        sustainability['ticker_id'] = self.ticker[0]
        sustainability = sustainability[columns]
        return sustainability

    def recommendations(self):
        recommendations = self.data[0].recommendations.reset_index()
        columns = recommendations.columns
        columns = columns.insert(0, 'ticker_id')
        recommendations['ticker_id'] = self.ticker[0]
        recommendations = recommendations[columns]
        recommendations =  recommendations.loc[recommendations['Date'] > datetime.today() - timedelta(weeks=72)]
        recommendations.columns = ['ticker_id', 'time', 'firm', 'toGrade', 'fromGrade', 'action']
        return recommendations

    def normalize(self, col):
        norm = []
        for i in col:
            i = i[0].lower() + i[1:]
            i = re.sub(' ', '', i)
            norm.append(i)
        return norm
