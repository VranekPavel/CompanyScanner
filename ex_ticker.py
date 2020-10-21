from yFin import YF
import sys
import os
import pandas as pd
import numpy as np
from yahooScrap import YahooFinanceTickers

ticker = [sys.argv[1]]
path = sys.argv[2]
target = sys.argv[3]
# ticker = ['AAPL']
#ticker= ['https://finance.yahoo.com/screener/predefined/growth_technology_stocks']
# path = r'C:\Users\Uzivatel\Documents\School\DiplomaThesis\Pythoning\excel'
# target = 'dashboard' # dashboard/screener

def merger(data, position):
    stock = pd.DataFrame(data.stock[0], index=[0])
    stock.set_index('ticker_id', inplace=True)
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
    output['shortTermInvestments'].astype('float64').replace(float('NaN'), 0, inplace=True)
    output['interestExpense'] = abs(output['interestExpense'])
    sector = data.market[0]['sector']
    if sector in [np.NaN, 'Consumer Goods', 'Financial', 'Industrial Goods', 'Services']:
        sector = 'Other'
    return output, sector

def count_stat(data):
    stat_counted = pd.DataFrame(index=data.index)
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
    stat_counted['cashSharesRatio'] = (data['cash'] + data['shortTermInvestments']) / data['sharesOutstanding']
    stat_counted['currentSharesRatio'] = data['totalCurrentAssets'] / data['sharesOutstanding']
    stat_counted['assetSharesRatio'] = data['totalAssets'] / data['sharesOutstanding']
    stat_counted['payoutRatio'] = (data['sharesOutstanding'] * data['dividendRate']) / data['netIncome']
    stat_counted['trailingPE'] = data['open'] / (data['netIncome']/data['sharesOutstanding'])
    stat_counted['priceToSalesTrailing12Months'] = (data['open'] / data['sharesOutstanding']) / (data['totalRevenue'] / data['sharesOutstanding'])
    stat_counted['enterpriseToRevenue'] = (data['sharesOutstanding'] * data['open'] + data['longTermDebt'] - data['cash'] - data['shortTermInvestments']) / data['totalRevenue']
    stat_counted['profitMargins'] = data['netIncome'] / data['totalRevenue']
    stat_counted['enterpriseToEbitda'] = (data['sharesOutstanding'] * data['open'] + data['longTermDebt'] - data['cash'] - data['shortTermInvestments']) / (data['ebit'] + data['depreciation'])
    stat_counted['trailingEps'] = data['netIncome'] / data['sharesOutstanding']
    try:
        stat_counted['heldPercentInstitutions'] = data['institutions'].str.replace('%', '').apply(lambda x: float(x) / 100)
    except Exception:
        stat_counted['heldPercentInstitutions'] = np.NaN
    #stat_counted['netIncomeToCommon'] = data['netIncome'] / data['sharesOutstanding']
    stat_counted['priceToBook'] = data['open'] / ((data['totalAssets'] - data['totalLiab']) / data['sharesOutstanding'])
    try:
        stat_counted['heldPercentInsiders'] = data['insiders'].str.replace('%', '').apply(lambda x: float(x) / 100)
    except Exception:
        stat_counted['heldPercentInsiders'] = np.NaN
    stat_counted['shortPercentOfFloat'] = data['sharesOutstanding'] / data['sharesShort']
    stat_counted['bookValue'] = data['totalAssets'] - data['totalLiab']
    stat_counted['marketCap'] = data['open'] * data['sharesOutstanding']    
    stat_counted['enterpriseValue'] = data['sharesOutstanding'] * data['open'] + data['longTermDebt'] - data['cash'] - data['shortTermInvestments']
    return stat_counted

def ticker_score(ticker_stats, data, sector):
    # ticker_stats - wanna count scores for them
    # data - ratios, used for count scores
    
    # žádoucí odchýlení
    #vyšší než mean
    up = ['currentRatio', 'quickRatio', 'cashRatio', 'timesInterestEarnedRatio', 'cashCoverageRatio', 'inventoryTurnover',
            'receivablesTurnover', 'totalAssetTurnover', 'profitMargins', 'ROA', 'ROE', 'cashSharesRatio', 'currentSharesRatio',
            'assetSharesRatio', 'trailingEps', 'heldPercentInsiders', 'shortPercentOfFloat']
    #menší než mean
    down = ['totalDebtRatio', 'debtEquityRatio', 'daysSalesInInventory', 'daysSalesInReceivables', 'daysSalesInTotalAssets',
                'capitalIntensity', 'priceToSalesTrailing12Months', 'enterpriseToRevenue', 'enterpriseToEbitda', 'heldPercentInstitutions',
                'priceToBook']
    #co nejblíže k mean (dát do abs)
    center =['equityMultiplier', 'trailingPE', 'market-bookRatio', 'payoutRatio']
    
    ticker_stats['sector'] = sector

    scores = pd.DataFrame(index=ticker_stats.index, columns = ticker_stats.columns[:35])
    for sector in ticker_stats['sector'].unique():
        sec_scores = pd.DataFrame()
        for col in ticker_stats.columns[:35]:
            middle = data.loc[(data['sector'] == sector) & (data[col] > data[col].describe(percentiles=[0.05]).loc['5%']) &
                        (data[col] < data[col].describe(percentiles=[0.95]).loc['95%']), col].mean()
            std = data.loc[(data['sector'] == sector) & (data[col] > data[col].describe(percentiles=[0.05]).loc['5%']) &
                        (data[col] < data[col].describe(percentiles=[0.95]).loc['95%']), col].std()
            sample = ticker_stats.loc[ticker_stats['sector'] == sector, col]
            if col in up:
                sec_scores.loc[sec_scores.index.isin(sample.index), col] = sample.apply(lambda x: (middle - x) / std)
            elif col in down:
                sec_scores.loc[sec_scores.index.isin(sample.index), col] = sample.apply(lambda x: (x - middle) / std)
            else:
                sec_scores.loc[sec_scores.index.isin(sample.index), col] = sample.apply(lambda x: (x - middle) / std) #po zaokrouhleni odecist jednicku od abs cisla
            if col in center:
                sec_scores = sec_scores.apply(lambda x: 1 - abs(x))
            sec_scores[sec_scores > 1] = 1
            sec_scores[sec_scores < -1] = -1
        scores.loc[scores.index.isin(sec_scores.index)] = sec_scores
    return scores

def prepare_data(tickers, iteration, start):
    # merge, count_stats
    # data - YF(ticker)
    # iteration - how many years to count
    # start - from which year start to prepare data
    counted_stats = pd.DataFrame()
    sector = []
    for ticker in tickers:
        try:
            data = YF(ticker)
        except Exception:
            continue
        for i in range(start, start + iteration):
            composed, sec = merger(data, i)
            sector.append(sec)

            stat_counted = count_stat(composed)
            
            if i == 0 & start == 0:
                stats = pd.Series(data.statistics[0])
                cols = stats[stats.notna()].index
                cols = cols[stats[cols].index.isin(stat_counted.columns)]
                stat_counted.loc[ticker, cols] = stats[cols]
            counted_stats = counted_stats.append(stat_counted)

    return counted_stats, sector

def dashboard(ticker, path, iteration):
    counted_stats, sector = prepare_data(ticker, iteration, 0 )
    counted_stats.index = [2020, 2019, 2018, 2017]
    counted_stats.to_csv(r'{}\data_source\company.csv'.format(path))

    data = YF(ticker[0])
    market = pd.Series(data.market[0])
    market['sector'] = sector[0]
    market.to_csv(r'{}\data_source\market.csv'.format(path), header=False)
    data.financials().to_csv(r'{}\data_source\financials.csv'.format(path))
    data.balance_sheet().to_csv(r'{}\data_source\balance.csv'.format(path))
    data.cashFlow().to_csv(r'{}\data_source\cf.csv'.format(path))
    data.stock_holders().to_csv(r'{}\data_source\stock_holders.csv'.format(path))
    data.historic().to_csv(r'{}\data_source\historic.csv'.format(path))
    pd.read_html('https://finance.yahoo.com/quote/{}/analysis'.format(ticker[0]))[5].to_csv(r'{}\data_source\estimators.csv'.format(path))
    pd.read_html('https://finance.yahoo.com/quote/{}/analysis'.format(ticker[0]))[2].to_csv(r'{}\data_source\estimators.csv'.format(path), mode='a')
    pd.read_html('https://finance.yahoo.com/quote/{}/analysis'.format(ticker[0]))[0].to_csv(r'{}\data_source\estimators.csv'.format(path), mode='a')
    pd.read_html('https://finance.yahoo.com/quote/{}/analysis'.format(ticker[0]))[1].to_csv(r'{}\data_source\estimators.csv'.format(path), mode='a')
    
    screener(ticker, path, 1, 0)


def screener(url, path, iteration, url_type=1):
    stats = pd.read_csv(r'{}\data_source\statistics.csv'.format(path))
    stats.set_index('ticker_id', inplace=True)
    if url_type == 1:
        tickers = YahooFinanceTickers(url).tickers()
    else:
        tickers = url

    ticker_stats, sector = prepare_data(tickers, iteration, 0)
    scores = ticker_score(ticker_stats, stats, sector)
    scores['sector'] = sector
    scores['trailingEPS'] = ticker_stats['trailingEps']
    grow_rate = pd.DataFrame(index=tickers, columns=['grow_rate'])
    for ticker in tickers:
        try:
            grow_rate.loc[ticker, 'grow_rate'] = pd.read_html('https://finance.yahoo.com/quote/{}/analysis'.format(ticker))[5].iloc[4, 1]
        except Exception:
            grow_rate['grow_rate'] = np.NaN
    scores = scores.merge(grow_rate, how='left', left_index=True, right_index=True)
    # try:
    #     os.remove(r'{}\data_source\screener.csv'.format(path))
    # except Exception:
    #     pass
    if url_type == 1:
        scores.to_csv(r'{}\data_source\screener.csv'.format(path))
    else:
        scores.to_csv(r'{}\data_source\score.csv'.format(path))

if target == 'screener':
    screener(ticker[0], path, 1)
else:
    dashboard(ticker, path, 4)