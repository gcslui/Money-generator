import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas
import pandas as pd
import sqlite3
import time

from src.db_class import DBCursor
from src.db_default import DB_VIS_TZ, DB_V1_PATH


def read_history(ticker, interval='minutes', sorting=None, as_dataframe=True):
    """
    Args:
    - sorting: if not None, must be a two-tuple of 'column_name', then 'ASC' or 'DESC'
    - as_dataframe: if False, return list of lists instead of dataframe
    Returns:
         pandas dataframe or list of lists from cursor.fetchall()
    """
    assert interval in ['days', 'minutes']
    tablename = '"%s_%s"' % (ticker, interval)
    cursor_exec = "SELECT * FROM %s" % tablename
    if sorting is not None:
        cursor_exec += ' ORDER BY %s %s' % (sorting[0], sorting[1])

    # args for pandas.to_datetime(...)
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
    if interval == 'dates':
        parse_dates = {}
    else:
        parse_dates = {'utc': True}

    if as_dataframe:
        conn = sqlite3.connect(DB_V1_PATH)
        out = pd.read_sql(cursor_exec, conn, index_col='date', parse_dates={'date': parse_dates})
        if interval == 'minutes':
            out.index = out.index.tz_convert(DB_VIS_TZ)

    else:
        with DBCursor(DB_V1_PATH) as cursor:
            cursor.execute(cursor_exec)
            out = cursor.fetchall()

    return out


def plot_timeseries(ticker, column='close', interval='minutes'):

    MAP_COLUMN_TO_LABEL = {
        'open': 'Price (open)',
        'high': 'Price (high)',
        'low': 'Price (low)',
        'close': 'Price (close)',
        'volume': 'Volume (units)',
    }

    df = read_history(ticker, interval=interval, sorting=['date', 'ASC'])

    title = '%s (%s) for interval: %s' % (ticker, column, interval)
    ylabel = MAP_COLUMN_TO_LABEL[column]

    plt.plot(np.arange(len(df)), df[column])
    plt.title(title); plt.ylabel(ylabel)
    plt.show()

    df[column].plot()
    plt.title(title); plt.ylabel(ylabel)
    plt.show()
    return


def plot_timeseries_fancy(ticker, style='yahoo', interval='minutes', vol=True, start=None, end=None):
    """ Uses mplfinance package to make OHLC candle plot with volume subplot

    ticker: is either a string (to a DB ticker) or a pandas DataFrame
        if string: try reading the default database for that ticker; this fetches a DataFrame
        if DataFrame: no need to load the database

    If vol: plot volume subplot below primary plot
    style options:
        'binance', 'blueskies', 'brasil', 'charles', 'checkers',
        'classic', 'default', 'mike', 'nightclouds', 'sas',
        'starsandstripes', 'yahoo']
    """

    if isinstance(ticker, str):
        df = read_history(ticker, interval=interval, sorting=['date', 'ASC'])
    else:
        assert isinstance(ticker, pandas.DataFrame)
        df = ticker

    # slicing df based on datetime intervals
    if start is not None:
        start = pd.to_datetime(start).tz_localize(DB_VIS_TZ)
        assert start >= df.index.min()
        df = df.loc[df.index > start]
    if end is not None:
        end = pd.to_datetime(end).tz_localize(DB_VIS_TZ)
        assert end <= df.index.max()
        df = df.loc[df.index < end]

    kwargs = {'type': 'candle',
              'style': style,
              'volume': vol,
              'title': '%s (interval: %s)' % (ticker, interval),
              'ylabel': 'Price ($)',
              'ylabel_lower': 'Volume',
              'tz_localize': True}
    if interval == 'days':
        kwargs['mav'] = (50, 200)
    if interval == 'minutes':
        kwargs['mav'] = (15, 60)
    mpf.plot(df, **kwargs)
    return


if __name__ == '__main__':
    ticker = 'AAPL'  # 'MSFT', 'CADUSD=X', 'BTC-USD'

    print(DB_V1_PATH)

    # Timing a table query
    stopwatch_start = time.time()
    fetch = read_history(ticker, interval='minutes', sorting=['date', 'ASC'], as_dataframe=False)
    print('Query took', time.time() - stopwatch_start, 'seconds')

    stopwatch_start = time.time()
    fetch = read_history(ticker, interval='minutes', sorting=['date', 'ASC'], as_dataframe=True)
    print('Query took', time.time() - stopwatch_start, 'seconds')
    print(fetch.dtypes)

    plot_timeseries_fancy(ticker, interval='days')
    plot_timeseries_fancy(ticker, interval='days', start='2016-09-01', end='2021-11-21')
    plot_timeseries_fancy(ticker, interval='minutes', start='2021-11-16', end='2021-11-18')
