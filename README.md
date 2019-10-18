## Investment

### Prerequisite

Get free api key of Alpha Vantage from [here](https://www.alphavantage.co/support/#api-key) and keep as format `AV_KET=<your key>` in the `.env` file.

### Rebalancing
Rebalancing is the process of realigning the weightings of a portfolio of assets.
> This involves periodically buying or selling assets in a portfolio to maintain an original or desired level of asset allocation or risk.

- Update your asset allocation in the `asset_allocation.csv` file.
- Update your cash at *line 11* in the `rebalancing.py`.
- Update your positions at *line 19* in the `rebalancing.py`.
- Run `python reblacing.py`. 
- Get the orders you need to process and latest status of portfolio.

### Backtesting
Backtesting is a term used in modeling to refer to testing a predictive model on historical data. 
> If backtesting works, traders and analysts may have the confidence to employ it going forward.

- Update your asset allocation in the `asset_allocation.csv` file.
- Update the date range as you wish at *line 13* in the `backtesting.py`.
- Run `python backtesting.py`. 
- Get the *ROI* within the date range and latest status of portfolio.

