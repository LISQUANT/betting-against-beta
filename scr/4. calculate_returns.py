# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:12:37 2026

@author: adria
"""

import pandas as pd
from pathlib import Path

# Load the weights and the daily returns
weights_df = pd.read_csv(Path('intermediary_steps') / 'final_portfolio_weights.csv')
daily_prices = pd.read_csv(Path('data') / 'stoxx600_yahoo_prices.csv', index_col='Date', parse_dates=True) 

daily_prices = daily_prices.sort_index()
daily_returns = daily_prices.pct_change(fill_method=None)

# Defragment the DataFrame
daily_returns = daily_returns.copy()

# Initialize the strategy column with zeros before adding the data
daily_returns['BAB_Strategy'] = 0.0
"""
It's a column with full of zeros
"""

# 2. Calculate daily returns for the whole strategy
# Using '_' to ignore the index and removing the 'if' statement
for _, row in weights_df.iterrows():
    stock_name = row['Stock']
    weight = row['Stock_Weight']
    
    # Add the profit/loss of this specific stock to our total strategy directly
    daily_returns['BAB_Strategy'] += daily_returns[stock_name].fillna(0) * weight
    """
    sum a column * (the constant weight) element by element to the colum of zeros
    fill NA with zero
    """
    
"""
for _, row in weights_df.iterrows():: This loops through your weights table one row at a time. The _ is a standard Python convention used to deliberately ignore the row's index number, as you only need the actual data contained in the row.

stock_name = row['Stock'] & weight = row['Weight']: These lines extract the specific company's name and its calculated leverage multiplier from the current row to use in the math below.

daily_returns['BAB_Strategy'] += daily_returns[stock_name] * weight: This executes the core financial calculation. It multiplies the stock's entire history of daily returns by your assigned weight. The += operator then adds that result into the master BAB_Strategy column, accumulating the data stock by stock until the total portfolio performance is built.

"""

# 3. Calculate cumulative growth (Compound interest)
# Adding 1 to convert raw decimals to multipliers (e.g., 0.02 -> 1.02)
daily_returns['Cumulative_BAB'] = (1 + daily_returns['BAB_Strategy']).cumprod()
"""
1 adds 1 to all the elements of the column

"""
# 4. Calculate final overall profit/loss percentage
final_growth_percentage = (daily_returns['Cumulative_BAB'].iloc[-1] - 1) * 100

"""
daily_returns['Cumulative_BAB'].iloc[-1]: The .iloc[-1] command tells Pandas to locate and extract the very last row of your cumulative growth column. This specific number represents the final total value of your initial 1-unit investment (e.g., 1€) at the exact end of your historical timeline.

- 1: Subtracting 1 strips away your original 100% starting capital. If your final portfolio value is 1.154, subtracting 1 isolates the pure profit as a raw decimal (0.154).

* 100: This multiplies the raw decimal by 100 to convert it into a standard, readable percentage format (turning 0.154 into 15.4%).

"""
print(f"Total Strategy Return: {final_growth_percentage:.2f}%\n")

# 5. Save the final backtesting results
results_path = Path('results') / 'final_strategy_results.csv'
daily_returns.to_csv(results_path, index=False)
print(f"Backtesting results successfully saved in '{results_path}'!")