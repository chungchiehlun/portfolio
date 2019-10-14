import pandas as pd
import numpy as np
import requests
import time
import os
from dotenv import load_dotenv, find_dotenv
from alpha_vantage.timeseries import TimeSeries

load_dotenv(find_dotenv())
API_KEY = os.environ.get('AV_KEY')

def instantiate_portfolio(targets, starting_balance):
  targets['CASH'] = 0
  tickers = list(targets.keys())

  df = pd.DataFrame(
    index=tickers,
    columns=[
      'date', 'price', 'target',
      'allocation', 'shares', 'market_value'
    ],
  )
  df.shares = 0
  df.market_value = 0
  df.allocation = 0
  df.update(
    pd.DataFrame
      .from_dict(targets, orient='index')
      .rename(columns={0:'target'})
  )
  df.at['CASH', 'shares'] = starting_balance

  return df

def deposit(portfolio, amount):
  portfolio.at['CASH', 'shares'] += amount
  portfolio.at['CASH', 'market_value'] = portfolio.at['CASH', 'shares']

def get_ticker_price(ticker, outputsize='compact', most_recent=False):
  URL='https://www.alphavantage.co/query?'
  payload = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': ticker,
    'apikey': API_KEY,
    'outputsize': outputsize
  }
  r = requests.get(URL, params=payload)
  p = pd.DataFrame(r.json()['Time Series (Daily)'])
  p = p.T['4. close']
  df = pd.DataFrame({ ticker: p.apply(float) })
  df.index = pd.to_datetime(df.index)
  if most_recent:
    return df.tail(1)
  return df

def get_prices(tickers, start_date, end_date):
  df = pd.DataFrame(index=pd.date_range(start_date, end_date, freq='D'))
  for t in tickers:
    # The API query 5 times at most every minute.
    time.sleep(15)
    df = pd.concat(
      [
        df,
        get_ticker_price(t, outputsize='full')
      ],
      axis=1,
      join_axes=[df.index]
    )
  df = df.fillna(method='ffill').dropna()
  return df

# close price of last trading sessions (60 min)
def get_latest_prices(tickers):
  ts = TimeSeries(key=API_KEY, output_format='pandas')
  # df = pd.DataFrame(index="latest")
  for i, t in enumerate(tickers):
    # The API query 5 times at most every minute.
    time.sleep(15)
    data, meta_data = ts.get_intraday(
      interval='60min', symbol=t
    )
    dt = data.tail(1)
    dt = dt.reset_index() \
    .loc[:, ['4. close']] \
    .rename(columns={ '4. close': t })

    if i == 0:
      df = dt
    else: 
      df = pd.concat(
        [
          df,
          dt
        ],
        axis=1,
        join_axes=[df.index]
      )
  return df.loc[0]
 

def update_prices(portfolio, prices):
  prices['CASH'] = 1
  portfolio.update(pd.DataFrame({'price': prices}))
  portfolio.date = prices.name
  portfolio.market_value = portfolio.shares * portfolio.price

def get_order(portfolio):
  total_value = portfolio.market_value.sum()
  order = (
    (total_value * portfolio.target // portfolio.price)
    - portfolio.shares
  ).drop('CASH')
  return order

def process_order(portfolio, order):
  starting_cash = portfolio.at['CASH', 'shares']
  cash_adjustment = np.sum(order * portfolio.price)
  portfolio.shares += order
  portfolio.at['CASH', 'shares'] = starting_cash - cash_adjustment
  portfolio.market_value = portfolio.shares * portfolio.price
  portfolio.allocation = (
    portfolio.market_value / portfolio.market_value.sum()
  )

