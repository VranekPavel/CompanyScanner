import psycopg2

def clear_environment():
    conn = psycopg2.connect('dbname=postgres user=postgres password=postgres')
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute('DROP DATABASE IF EXISTS fin_data')
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

    cur.execute("CREATE USER uzivatel WITH ENCRYPTED PASSWORD 'postgres'")
    cur.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO uzivatel')
    cur.execute('ALTER SCHEMA public OWNER TO uzivatel')

    conn.close()

def create_schema():
    conn = psycopg2.connect('dbname=fin_data user=postgres password=postgres')
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Market(
            industry varchar(50),
            sector varchar(50),
            PRIMARY KEY (industry, sector)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Company(
            ticker_id varchar(6) PRIMARY KEY,
            name varchar(50),
            address varchar(256),
            web varchar(256),
            contact varchar(50),
            sector varchar(50),
            industry varchar(50),
            num_of_employees integer,
            FOREIGN KEY (sector, industry) REFERENCES Market(sector, industry)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Balance_sheet(
            id serial PRIMARY KEY,
            ticker varchar(6),
            time date,
            time_period varchar(10),
            cash integer,
            receivables integer,
            inventory integer,
            current_assets integer,
            non_current_assets integer,
            FOREIGN KEY (ticker) REFERENCES Company(ticker_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Stock(
            ticker varchar(6) PRIMARY KEY,
            previous_close integer,
            open integer,
            bid integer,
            ask integer,
            day_range varchar(50),
            week_range_52 varchar(50),
            volume integer,
            volume_avg integer,
            FOREIGN KEY (ticker) REFERENCES Company(ticker_id)
        )
    ''')
    conn.close() 

try:
    #clear_environment()
    #create_database()
    #create_schema()
    create_user()
except Exception as error:
        print(error)
