# Scanner for publicly traded companies

Aim of this application is to analyze public companies and suggest best for investing

* postgres.py - Database inicialization, tables, users
* yFin.py - transformation of data objects from yFinance (yfinance_master)
* inserter.py - inserting data into database
* run.py - interface
* yahooScrap.py - scraping data from yahoo Finance
* ex_ticker.py - performes final calculations with outcomes to csv files

# Jupyter files
Jupyter notebooks contains data analysis 
* preprocessing - preparing data for actual analysis and for use in tool
* model_ratio - model for scoring companies
* model_ML - Machine Learning model for prediction of stock price change based of fundamental analysis
