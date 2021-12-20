import os
import sys


# file io - directory structure and system path
SRC_DIR = os.path.dirname(__file__)                          # abspath root/src/
PROJECT_ROOT = os.path.dirname(SRC_DIR)                      # abspath root/
sys.path.append(PROJECT_ROOT)

# file io - specific file locations
DB_DIR = PROJECT_ROOT + os.sep + 'financial_db'                  # db_path files are stored here
DB_V1_PATH = DB_DIR + os.sep + 'default_finance_v1.db'           # intended as a 'frozen' database

DB_TABLES = ['''security (
                    ticker TEXT PRIMARY KEY,
                    name_short TEXT,
                    name_long TEXT,
                    exchange TEXT,
                    currency TEXT,
                    type TEXT,
                    sector TEXT,
                    industry TEXT,
                    market TEXT,
                    hq_country TEXT,
                    employees INT,
                    website TEXT,
                    FOREIGN KEY(exchange) REFERENCES exchange (exchange_name)
                    ) ''',
             '''exchange (
                    exchange_name TEXT PRIMARY KEY,
                    exchange_timezone TEXT,
                    exchange_timezone_short TEXT
                    )''',
             '''price_daily (
                    date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    adjusted_close REAL,
                    volume INTEGER,
                    security_ticker TEXT,
                    CONSTRAINT price_day_key PRIMARY KEY (security_ticker, date),
                    FOREIGN KEY(security_ticker) REFERENCES security (ticker)
                    )''',
             '''price_minutely (
                    date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    adjusted_close REAL,
                    volume INTEGER,
                    security_ticker TEXT,
                    CONSTRAINT price_min_key PRIMARY KEY (security_ticker, date),
                    FOREIGN KEY(security_ticker) REFERENCES security (ticker)
                    )''',
             '''actions (
                    date TEXT,
                    dividends REAL,
                    stock_splits REAL,
                    security_ticker TEXT,
                    CONSTRAINT actions_key PRIMARY KEY (security_ticker, date),
                    FOREIGN KEY(security_ticker) REFERENCES security (ticker)
                    )'''
             ]

DB_ASSUMED_TZ = 'US/Eastern'  # TODO currently used in visualize.py; assumed all database times are in US/Eastern

# TODO implement with hashing: where to read/record the hash?
# TODO e.g. have a db_generate.py which A) creates a variant if it does not exist B) checks hash otherwise
DB_FROZEN_VARIANTS = {
    'mixed_v1':
        {'tickers': ['MSFT', 'AAPL', 'HUT', 'HUT.TO', 'SPY', 'CADUSD=X', 'BTC-USD', 'ETH-USD', 'ETHX-U.TO'],
         'db_filename': 'default_mixed_v1.db',
         'hash': 'TODO'}
}

DB_TICKERS = ['MSFT', 'AAPL', 'HUT', 'HUT.TO', 'SPY', 'CADUSD=X', 'BTC-USD', 'ETH-USD', 'ETHX-U.TO']
