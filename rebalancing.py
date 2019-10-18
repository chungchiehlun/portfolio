import pandas as pd
import portfolio as pf

# https://stackoverflow.com/a/47668182/5254013
targets = pd.read_csv('asset_allocation.csv', header=0, index_col=0, squeeze=True).to_dict()

# Get latest prices
prices = pf.get_latest_prices(targets.keys())

# Initialize portfolio with cash $10,000 USD
cash = 1458
portfolio = pf.instantiate_portfolio(targets, cash)

# Initailize shares
shares = pd.DataFrame({ "shares": portfolio.shares })
shares.at['CASH', 'shares'] = cash 

# Add shares
shares.at['GLD', 'shares'] = 10
shares.at['IWM', 'shares'] = 10
shares.at['QQQ', 'shares'] = 8
shares.at['SCHD', 'shares'] = 28
shares.at['VEA', 'shares'] = 37
shares.at['VOO', 'shares'] = 5 

portfolio.shares = shares.shares

# Deposit
# deposit_cash = 1000
# pf.deposit(portfolio, deposit_cash)

# Update prices
pf.update_prices(portfolio, prices)
order = pf.get_order(portfolio)
print("{0}".format(order))
pf.process_order(portfolio, order)

print(portfolio)

