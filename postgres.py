import psycopg2

def clear_environment():
    conn = psycopg2.connect('dbname=fin_data user=postgres password=postgres')
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute('DROP SCHEMA IF EXISTS public CASCADE')
    cur.execute('DROP USER IF EXISTS uzivatel')
    conn.close()

def create_database():
    conn = psycopg2.connect('dbname=postgres user=postgres password=postgres')
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute('CREATE DATABASE fin_data')

    conn.close()

def create_user():
    conn = psycopg2.connect('dbname=fin_data user=postgres password=postgres')
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("CREATE USER uzivatel WITH PASSWORD 'postgres'")
    cur.execute('GRANT USAGE ON SCHEMA public TO uzivatel')
    cur.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO uzivatel')
    cur.execute('GRANT SELECT, USAGE, UPDATE ON ALL SEQUENCES IN SCHEMA public TO uzivatel')

    conn.close()

def create_schema():
    conn = psycopg2.connect('dbname=fin_data user=postgres password=postgres')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('CREATE SCHEMA IF NOT EXISTS public')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Company(
            ticker_id varchar(15) PRIMARY KEY,
            "shortName" varchar(50),
            "longName" varchar(256),
            zip varchar(50),
            "fullTimeEmployees" bigint,
            "longBusinessSummary" text,
            city varchar(50),
            phone varchar(50),
            state varchar(50),
            country varchar (100),
            website varchar(256),
            address varchar(256),
            "isEsgPopulated" boolean,
            "quoteType" varchar(20),
            market varchar(50),
            "morningStarRiskRating" varchar(50),
            "fundFamily" varchar(50),
            "lastFiscalYearEnd" bigint,
            "nextFiscalYearEnd" bigint,
            "mostRecentQuarter" bigint,
            "legalType" varchar(50),
            "morningStarOverallRating" varchar(50)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Market(
            ticker_id varchar(15) PRIMARY KEY,
            industry varchar(50),
            sector varchar(50),
            FOREIGN KEY (ticker_id) references Company(ticker_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Stock(
            ticker_id varchar(15) PRIMARY KEY,
            currency varchar(6),
            exchange varchar(6),
            "exchangeTimezoneName" varchar(50),
            "exchangeTimezoneShortName" varchar(6),
            open float(8),
            bid float(8),
            "bidSize" float(8),
            "dayHigh" float(8),
            "dayLow" float(8),
            ask float(8),
            "askSize" float(8),
            "previousClose" float(8),
            "regularMarketOpen" float(8),
            "regularMarketPrice" float(8),
            "regularMarketPreviousClose" float(8),
            "regularMarketDayHigh" float(8),
            "regularMarketDayLow" float(8),
            "regularMarketVolume" float(8),
            volume float(8),
            "averageVolume" float(8),
            "averageDailyVolume10Day" float(8),
            "averageVolume10days" float(8),
            "fiftyTwoWeekHigh" float(8),
            "fiftyTwoWeekLow" float(8),
            "fiftyTwoWeekChange"float(8),
            "fiftyDayAverage" float(8),
            "twoHundredDayAverage" float(8),
            "ytdReturn" float(8),
            "sharesOutstanding" float(8),
            "sharesPercentSharesOut" float(8),
            "SandP52WeekChange" float(8),
            "sharesShort" float(8),
            "sharesShortPreviousMonthDate" bigint,
            "sharesShortPriorMonth" float(8),
            "floatShares" float(8),
            "lastSplitDate" bigint,
            "lastSplitFactor" varchar(20),
            "trailingAnnualDividendYield" float(8),
            "trailingAnnualDividendRate" float(8),
            yield float(8),
            "fiveYearAvgDividendYield" float(8),
            "dividendYield" float(8),
            "dividendRate" float(8),
            "exDividendDate" bigint,
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Statistics(
            ticker_id varchar(15) PRIMARY KEY,
            "payoutRatio" float(8),
            beta float(8),
            "beta3Year" float(8),
            "trailingPE" float(8),
            "forwardPE" float(8),
            "priceToSalesTrailing12Months" float(8),
            "enterpriseToRevenue" float(8),
            "profitMargins" float(8),
            "enterpriseToEbitda" float(8),
            "forwardEps" float(8),
            "heldPercentInstitutions" float(8),
            "netIncomeToCommon" float(8),
            "trailingEps" float(8),
            "priceToBook" float(8),
            "heldPercentInsiders" float(8),
            "shortRatio" float(8),
            "threeYearAverageReturn" float(8),
            "earningsQuarterlyGrowth" float(8),
            "revenueQuarterlyGrowth" float(8),
            "pegRatio" float(8),
            "lastCapGain" bigint,
            "shortPercentOfFloat" float(8),
            "fiveYearAverageReturn" float(8),
            "bookValue" float(8),
            "marketCap" bigint,
            "enterpriseValue" bigint,
            "annualHoldingsTurnover" bigint,
            "totalAssets" bigint, 
            "circulatingSupply" bigint,
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)       
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Dividends(
            id serial PRIMARY KEY,
            ticker_id varchar(15),
            time date,
            value float(8),
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Financials(
            id serial PRIMARY KEY,
            ticker_id varchar(15),
            "timePeriod" varchar(20),
            time date,
            "researchDevelopment" bigint,
            "accountingCharges" bigint,
            "incomeBeforeTax" bigint,
            "minorityInterest" bigint,
            "netIncome" bigint,
            "sellingGeneralAdministrative" bigint,
            "grossProfit" bigint,
            ebit bigint,
            "operatingIncome" bigint,
            "otherOperatingExpenses" bigint,
            "interestExpense" bigint,
            "extraordinaryItems" bigint,
            "nonRecurring" bigint,
            "otherItems" bigint,
            "incomeTaxExpense" bigint,
            "totalRevenue" bigint,
            "totalOperatingExpenses" bigint,
            "costOfRevenue" bigint,
            "totalOtherIncomeExpenseNet" bigint,
            "discontinuedOperations" bigint,
            "netIncomeFromContinuingOps" bigint,
            "netIncomeApplicableToCommonShares" bigint,
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Stock_holders(
            id serial PRIMARY KEY,
            ticker_id varchar(15),
            insiders varchar(10),
            institutions varchar(10),
            institutions_float varchar(10),
            "numOfInstitutions" integer,
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Balance_sheet(
            id serial PRIMARY KEY,
            time date,
            "totalLiab" bigint,
            "totalStockholderEquity" bigint,
            "otherCurrentLiab" bigint,
            "totalAssets" bigint,
            "commonStock" bigint,
            "otherCurrentAssets" bigint,
            "retainedEarnings" bigint,
            "otherLiab" bigint,
            "treasuryStock" bigint,
            "otherAssets" bigint,
            cash bigint,
            "totalCurrentLiabilities" bigint,
            "shortLongTermDebt" bigint,
            "otherStockholderEquity" bigint,
            "propertyPlantEquipment" bigint,
            "totalCurrentAssets" bigint,
            "longTermInvestments" bigint,
            "netTangibleAssets" bigint,
            "shortTermInvestments" bigint,
            "netReceivables" bigint,
            "longTermDebt" bigint,
            "inventory" bigint,
            "accountsPayable" bigint,
            "intangibleAssets" bigint,
            "goodWill" bigint,
            "deferredLongTermAssetCharges" bigint,
            "deferredLongTermLiab" bigint,
            "capitalSurplus" bigint,
            "minorityInterest" bigint,
            ticker_id varchar(15),
            "timePeriod" varchar(10),
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS cash_flow(
            id serial PRIMARY KEY,
            ticker_id varchar(15),
            "timePeriod" varchar(10),
            time date,
            investments bigint,
            "changeToLiabilities" bigint,
            "totalCashflowsFromInvestingActivities" bigint,
            "netBorrowings" bigint,
            "totalCashFromFinancingActivities" bigint,
            "changeToOperatingActivities" bigint,
            "issuanceOfStock" bigint,
            "netIncome" bigint,
            "changeInCash" bigint,
            "repurchaseOfStock" bigint,
            "totalCashFromOperatingActivities" bigint,
            depreciation bigint,
            "otherCashflowsFromInvestingActivities" bigint,
            "dividendsPaid" bigint,
            "changeToInventory" bigint,
            "changeToAccountReceivables" bigint,
            "otherCashflowsFromFinancingActivities" bigint,
            "changeToNetincome" bigint,
            "capitalExpenditures" bigint,
            "effectOfExchangeRate" bigint,
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)
     )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Earnings(
            id serial PRIMARY KEY,
            ticker_id varchar(15),
            "timePeriod" varchar(20),
            "year" varchar(6),
            "revenue" bigint,
            "earnings" bigint,
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Sustainability(
            ticker_id varchar(15) PRIMARY KEY,
            "palmOil" boolean,
            "controversialWeapons" boolean,
            gambling boolean,
            "socialScore" bigint,
            nuclear boolean,
            "furLeather" boolean,
            alcoholic boolean,
            gmo boolean,
            catholic boolean,
            "socialPercentile" float(2),
            "peerCount" bigint,
            "governanceScore" float(2),
            "environmentPercentile" float(2),
            "animalTesting" boolean,
            tobacco boolean,
            "totalEsg" float(2),
            "highestControversy" bigint,
            "esgPerformance" varchar(20),
            coal boolean,
            pesticides boolean,
            adult boolean,
            percentile float(2),
            "peerGroup" varchar(50),
            "smallArms" boolean,
            "environmentScore" float(2),
            "governancePercentile" float(2),
            "militaryContract" boolean,
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Recommendations(
            id serial PRIMARY KEY,
            ticker_id varchar(15),
            time date,
            firm varchar(250),
            "toGrade" varchar(20),
            "fromGrade" varchar(20),
            action varchar(20),
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS stock_tseries(
            id serial PRIMARY KEY,
            ticker_id varchar(15),
            time date,
            open float(8),
            high float(8),
            low float(8),
            close float(8),
            volume bigint,
            FOREIGN KEY (ticker_id) REFERENCES Company(ticker_id)
        )
    ''')
    conn.close() 

try:
    #create_database()
    clear_environment()
    create_schema()
    create_user()
except Exception as error:
    print(error)
else:
    print('success')
