import pandas as pd
import portfolio as pf

# https://stackoverflow.com/a/47668182/5254013
targets = pd.read_csv('asset_allocation.csv', header=0, index_col=0, squeeze=True).to_dict()

# get historical prices and set time range of portfolio reb
historical_prices = pf.get_prices(
  tickers = targets.keys(),
  start_date = pd.Timestamp(2017, 1, 1),
  end_date = pd.Timestamp.today().normalize()
)
dates = pd.date_range('2017-09-30', '2019-09-30', freq='Q').tolist()

# initialize portfolio
portfolio = pf.instantiate_portfolio(targets, 10000)

for i, d in enumerate(dates):
  prices = historical_prices.loc[d]
  if i ==  1:
    cost_of_investment = portfolio.market_value.sum() - portfolio.loc['CASH', 'market_value'] 

  pf.update_prices(portfolio, prices)
  order = pf.get_order(portfolio)
  # print(f'{d}:\n{order}')
  pf.process_order(portfolio, order)

current_value_of_investment = portfolio.market_value.sum() - portfolio.loc['CASH', 'market_value'] 

print(portfolio)
print(
"ROI: {:.1%}".format((current_value_of_investment - cost_of_investment) /cost_of_investment)
)

