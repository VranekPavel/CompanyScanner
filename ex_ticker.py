from yFin import YF
import sys
import os
import pandas as pd
import numpy as np

# ticker = sys.argv[1]
# path = sys.argv[2]
ticker= 'AAPL'
path = r'C:\Users\Uzivatel\Documents\School\DiplomaThesis\Pythoning\excel'
data = YF(ticker)
stock = pd.DataFrame(data.stock[0], index=[0])
stock.set_index('ticker_id', inplace=True)
stats = pd.Series(data.statistics[0])

def merger(position):
    output = stock.merge(
        data.financials().groupby('ticker_id').nth(position),
        how='left',
        on='ticker_id')
    output = output.merge(
        data.stock_holders(),
        how='left',
        on='ticker_id')
    output = output.merge(
        data.balance_sheet().groupby('ticker_id').nth(position),
        how='left',
        on='ticker_id',
        suffixes=('', '_bs'))
    output = output.merge(
        data.cashFlow().groupby('ticker_id').nth(position),
        how='left',
        on='ticker_id',
        suffixes=('','_cf'))
    output.set_index('ticker_id', inplace=True)
    
    output.replace({0:float('NaN'), None: float('NaN')}, inplace=True)
    output['shortTermInvestments'].replace(float('NaN'), 0, inplace=True)
    output['interestExpense'] = abs(output['interestExpense'])
    return output

def count_stat(data):
    stat_counted = pd.Series(dtype='object')
    stat_counted['currentRatio'] = data['totalCurrentAssets'] / data['totalCurrentLiabilities']
    stat_counted['quickRatio'] = (data['totalCurrentAssets'] - data['inventory']) / data['totalCurrentLiabilities']
    stat_counted['cashRatio'] = data['cash'] / data['totalCurrentLiabilities']
    stat_counted['totalDebtRatio'] = (data['totalAssets'] - data['totalStockholderEquity']) / data['totalAssets']
    stat_counted['debtEquityRatio'] = (data['longTermDebt'] + data['shortLongTermDebt']) / data['totalStockholderEquity']
    stat_counted['equityMultiplier'] = data['totalAssets'] / data['totalStockholderEquity']
    stat_counted['timesInterestEarnedRatio'] = data['ebit'] / data['interestExpense']
    stat_counted['cashCoverageRatio'] = (data['ebit'] + data['depreciation']) / data['interestExpense']
    stat_counted['inventoryTurnover'] = data['costOfRevenue'] / data['inventory']
    stat_counted['daysSalesInInventory'] = 365 / stat_counted['inventoryTurnover']
    stat_counted['receivablesTurnover'] = data['totalRevenue'] / data['netReceivables']
    stat_counted['daysSalesInReceivables'] = 365 / stat_counted['receivablesTurnover']
    stat_counted['totalAssetTurnover'] = data['totalRevenue'] / data['totalAssets']
    stat_counted['daysSalesInTotalAssets'] = 365 / stat_counted['totalAssetTurnover']
    stat_counted['capitalIntensity'] = data['totalAssets'] / data['totalRevenue']
    stat_counted['ROA'] = data['netIncome'] / data['totalAssets']
    stat_counted['ROE'] = data['netIncome'] / data['totalStockholderEquity']
    stat_counted['market-bookRatio'] = (data['open'] * data['sharesOutstanding'])  / ((data['totalAssets'] - data['totalLiab']) / data['sharesOutstanding'])
    stat_counted['cashSharesRatio'] = data['cash'] / data['sharesOutstanding']
    stat_counted['currentSharesRatio'] = data['totalCurrentAssets'] / data['sharesOutstanding']
    stat_counted['assetSharesRatio'] = data['totalAssets'] / data['sharesOutstanding']
    stat_counted['payoutRatio'] = (data['sharesOutstanding'] * data['dividendRate']) / data['netIncome']
    stat_counted['trailingPE'] = data['open'] / (data['netIncome']/data['sharesOutstanding'])
    stat_counted['priceToSalesTrailing12Months'] = data['sharesOutstanding'] / data['totalRevenue']
    stat_counted['enterpriseToRevenue'] = (data['sharesOutstanding'] * data['open'] + data['longTermDebt'] - data['cash'] - data['shortTermInvestments']) / data['totalRevenue']
    stat_counted['profitMargins'] = data['netIncome'] / data['totalRevenue']
    stat_counted['enterpriseToEbitda'] = (data['sharesOutstanding'] * data['open'] + data['longTermDebt'] - data['cash'] - data['shortTermInvestments']) / (data['ebit'] + data['interestExpense'] + data['incomeTaxExpense'])
    stat_counted['trailingEps'] = data['sharesOutstanding'] / data['netIncome']
    stat_counted['heldPercentInstitutions'] = data['institutions'].replace('%', '')
    #stat_counted['netIncomeToCommon'] = data['netIncome'] / data['sharesOutstanding']
    stat_counted['priceToBook'] = data['open'] / ((data['totalAssets'] - data['totalLiab']) / data['sharesOutstanding'])
    stat_counted['heldPercentInsiders'] = data['insiders'].replace('%', '')
    stat_counted['shortPercentOfFloat'] = data['sharesOutstanding'] / data['sharesShort']
    stat_counted['bookValue'] = (data['totalAssets'] - data['totalLiab']) / data['sharesOutstanding']
    stat_counted['marketCap'] = data['open'] * data['sharesOutstanding']    
    stat_counted['enterpriseValue'] = data['sharesOutstanding'] * data['open'] + data['longTermDebt'] - data['cash'] - data['shortTermInvestments']
    return stat_counted

counted_stats = pd.DataFrame(columns=[2019, 2018, 2017, 2016])
for i in range(4):
    composed = merger(i)
    composed = pd.Series(composed.values[0], index=composed.columns)
    stat_counted = count_stat(composed)

    cols = stats[stats.notna()].index
    cols = cols[stats[cols].index.isin(stat_counted.index)]

    stat_counted[cols] = stats[cols]
    counted_stats[2019 - i] = stat_counted


counted_stats.to_csv(r'{}\data_source\company.csv'.format(path))

market = pd.Series(data.market[0])
if market['sector'] in [np.NaN, 'Consumer Goods', 'Financial', 'Industrial Goods', 'Services']:
    market['sector'] = 'Other'
market.to_csv(r'{}\data_source\market.csv'.format(path), header=False)
data.financials().to_csv(r'{}\data_source\financials.csv'.format(path))
data.balance_sheet().to_csv(r'{}\data_source\balance.csv'.format(path))
data.cashFlow().to_csv(r'{}\data_source\cf.csv'.format(path))
data.stock_holders().to_csv(r'{}\data_source\stock_holders.csv'.format(path))
data.historic().to_csv(r'{}\data_source\historic.csv'.format(path))
pd.read_html('https://finance.yahoo.com/quote/{}/analysis'.format(ticker))[5].to_csv(r'{}\data_source\estimators.csv'.format(path))
