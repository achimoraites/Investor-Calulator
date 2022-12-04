import csv
import sqlite3


def read_csv(path):
    data = list()
    with open(path, 'r') as file:
        reader = csv.DictReader(file, delimiter=",")

        for line in reader:
            for i in line:
                if line[i] is '':
                    line[i] = None
            data.append(line)

    return data


def init_db(db='investor.db', companies_csv='companies.csv', financial_csv='financial.csv', log=False):

    companies = read_csv(companies_csv)
    financial = read_csv(financial_csv)
    
    con = sqlite3.connect(db)
    cursor = con.cursor()
    
    populate_companies_table(companies, con, cursor)
    populate_financial_table(con, cursor, financial)
    
    cursor.close()
    con.close()
    
    if log:
        print('Database created successfully!')


def populate_companies_table(companies, con, cursor):
    # create the companies table
    cursor.execute("""CREATE TABLE IF NOT EXISTS companies(
         ticker TEXT PRIMARY KEY,
         name TEXT,
         sector TEXT
         );""")
    for c in companies:
        entry = (c['ticker'], c['name'], c['sector'])
        try:
            cursor.execute("INSERT INTO companies(ticker, name, sector) VALUES (?, ?, ?)", entry)
        except sqlite3.IntegrityError:
            # duplicate entry
            pass
    con.commit()


def populate_financial_table(con, cursor, financial):
    # create the financial table
    cursor.execute("""CREATE TABLE IF NOT EXISTS financial(
         ticker TEXT PRIMARY KEY,
         ebitda REAL,
         sales REAL,
         net_profit REAL,
         market_price REAL,
         net_debt REAL,
         assets REAL,
         equity REAL,
         cash_equivalents REAL,
         liabilities REAL
         );""")

    for f in financial:
        entry = (f['ticker'], f['ebitda'], f['sales'], f['net_profit'], f['market_price'],
                 f['net_debt'], f['assets'], f['equity'], f['cash_equivalents'], f['liabilities'])
        try:
            cursor.execute("""
            INSERT INTO financial(
            ticker,
            ebitda, 
            sales, 
            net_profit, 
            market_price, 
            net_debt, 
            assets, 
            equity, 
            cash_equivalents, 
            liabilities) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", entry)
        except sqlite3.IntegrityError:
            # duplicate entry
            pass
    con.commit()
