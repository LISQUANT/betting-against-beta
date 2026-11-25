# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 12:23:00 2026

@author: adria
"""

import pandas as pd
import numpy as np
from pathlib import Path

# 1. Load the generated data
csv_path = Path('data')/ 'stoxx600_yahoo_prices.csv'
df = pd.read_csv(csv_path, index_col='Date', parse_dates=True)

"""
index_col='Date': Tells Python that the column named "Date" is not regular data, but the main index (the spine or row labels of the table). This ensures every single row is identified by its specific day.

parse_dates=True: Tells Python: "Pay attention, the items in the index are real calendar dates, not just plain text." This is crucial so the program understands the chronological flow of time (which day comes before or after another).
"""


# Ensure dates are sorted from oldest to newest
df = df.sort_index()

# Convert all prices to numeric values
df = df.apply(pd.to_numeric, errors='coerce')


"""
df.apply() — applies a function (pd.numeric) to every column in the DataFrame (in this case each intex/stock returns)
pd.to_numeric - converts values to numeric values (if already numeric doesn't do anything)
errors='coerce' - if can't convert (in our case empty values) converts to NaN
"""

# Remove invalid non-positive prices
df = df.where(df > 0)
"""
Our values should already be positive (just a safety precaution)
df.where() - keeps values when the codition is true, otherwise replaces them with NaN
"""


# 2. Calculate daily percentage returns
returns = df.pct_change(fill_method=None)

"""
fill_method=None:
- Missing prices are not automatically replaced with previous prices.
- If either today's or yesterday's price is missing, the corresponding return remains NaN.
"""


# 3. Separate the index (market) from the stocks
market_returns = returns['INDEX']
stock_returns = returns.drop(columns=['INDEX'])

# 4. Calculate the Beta for each stock
betas = {}
var_market = market_returns.var()

for col in stock_returns.columns:

    stock = stock_returns[col]

    valid = stock.notna() & market_returns.notna()

    stock_valid = stock.where(valid)
    market_valid = market_returns.where(valid)

    cov_stock = stock_valid.cov(market_valid)

    var_market = market_valid.var()

    beta = cov_stock / var_market

    betas[col] = beta


"""
The variable col temporarily holds the name of the current company being analyzed (for example, "Stock_APPLE").

valid - is a vector of True/False's
      - its True for a date (index) only if both stock_return and market_return are not NA (if both exist)  

stock_valid / market_valid - respective returns without non valid indices

variance is calculated for each stock, because each stock has is own valid rows

This calculates the "covariance" (.cov()) between the specific stock and the overall market index. Covariance is a statistical tool that measures how closely the daily price changes of this stock match the daily price changes of the market.
(HAVE IN MIND, ARE TWO COLUMS)

What it does: It takes that final Beta number and saves it inside the betas dictionary
"""

# 5. Display results
df_betas = pd.DataFrame(list(betas.items()), columns=['Stock', 'Beta'])
print("\n--- CALCULATED BETAS ---")
print(df_betas)
"""
betas.items(): The betas variable is a Python dictionary (which stores data in pairs, like Company: Beta). This command extracts all those pairs together (e.g., "Apple" and "1.12").

list(...): This takes those extracted pairs and bundles them into a standard, ordered Python list so that Pandas can read them easily.

pd.DataFrame(...): This is the core Pandas command that takes your raw list of data and transforms it into a clean, two-dimensional table (a DataFrame) with rows and columns.

columns=['Stock', 'Beta']: This assigns specific names to the columns of your new table. The company names will go under the header "Stock", and their corresponding risk numbers will go under "Beta".

df_betas = : Finally, this saves the fully built table into a new variable named

"""

# Save the calculated betas for the next step
calculated_betas_path = Path('intermediary_steps') / 'calculated_betas.csv'
df_betas.to_csv(calculated_betas_path, index=False)
print(f"\nBetas successfully saved in {calculated_betas_path}")