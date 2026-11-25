# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 12:47:43 2026

@author: adria
"""
import pandas as pd
from pathlib import Path

# 1. Set the data folder path and load the calculated betas
calculated_betas_path = Path('intermediary_steps') / 'calculated_betas.csv'
df_betas = pd.read_csv(calculated_betas_path)

# Remove stocks with missing betas
df_betas = df_betas.dropna(subset=['Beta']).copy()

# 2. Sort stocks from lowest to highest beta
df_betas = df_betas.sort_values('Beta')

# 3. Split the companies into ten groups
df_betas['Beta_Group'] = pd.qcut(
    df_betas['Beta'].rank(method='first'),
    q=10,
    labels=range(1, 11)
)

"""
We will divide the stock into 10 groups (5 to buy, 5 to sell)
qcut - divides this automatically

.rank(method='first')	Ranks the stocks and resolves identical beta values using their row order
q = 10                  Divides the stocks into ten approximately equal-sized groups
labels=range(1, 11)     Names the groups from 1 to 10

creates a new column 'Beta Group' in our df where the beta group of our stock is safe
Stock / Beta / Beta Group
APPLE   1.5        3
...
"""


# 4. Save all stocks with their respective beta groups
folder_path = Path('intermediary_steps')

df_betas.to_csv( folder_path / 'beta_groups.csv', index=False)

#NOT REALLY PORTFOLIOS (THERE ARE NOT WEIGHTS YET TO DETERMINE A STRATEGY OF INVESTMENT), JUST DATA (STOCKS WITH THEIR RESPECTIVE BETA)
print(f"\nAll beta groups successfully saved in {folder_path}")
