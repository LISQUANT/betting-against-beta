# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 12:57:35 2026

@author: adria
"""

import pandas as pd
import numpy as np
from pathlib import Path

# 1. Set the folder path and load the beta groups from Step 2
folder_path = Path('intermediary_steps')
beta_groups_path = folder_path / 'beta_groups.csv'

df_betas = pd.read_csv(beta_groups_path)
""" Betas = Stock / Beta / Beta Group

We will create a new df groups
Groups = Beta Group / Average Beta / Num Stocks Inverse Beta

"""


# 2. Calculate the average beta of each group
df_groups = df_betas.groupby('Beta_Group')['Beta'].mean().reset_index()
""" groupby joins stocks by beta group, then we save the average of the betas """

df_groups = df_groups.rename(columns={'Beta': 'Average_Beta'})


# 3. Calculate the number of stocks in each group
num_stocks = df_betas.groupby('Beta_Group').size() 

df_groups['Num_Stocks'] = df_groups['Beta_Group'].map(num_stocks)

# 4. Calculate the inverse beta
# Negative inverse beta for groups 6-10 (we want to short(sell) high betas)
df_groups['Inverse_Beta'] = np.where(
    df_groups['Beta_Group'] >= 6,
    -1 / df_groups['Average_Beta'],
    1 / df_groups['Average_Beta']
)

# 5. Calculate the weight of each group
# Inverse_Beta/5 * Beta = 1/5 for each of the five groups = 1
df_groups['Weight'] = df_groups['Inverse_Beta'] / 5

# 6. Calculate the weight of each stock within the group
# We consider stocks within the same group as equals
df_groups['Stock_Weight'] = (
    df_groups['Weight'] / df_groups['Num_Stocks']
)

# 7. Add the individual stock weights to df_betas
df_betas = df_betas.merge(
    df_groups[['Beta_Group', 'Stock_Weight']],
    on='Beta_Group',
    how='left'
)
""" 
merge will merge df_betas with the columns ['Beta_Group', 'Stock_Weight'] of df_groups
on='Beta_Group' — specifies the common column used to match the rows.
how='left' — keeps every stock from the original df_betas, even if there is no matching group (in which case its weight becomes NaN).
"""

# 8. Save the final portfolio weights
group_weights_path = folder_path / 'final_portfolio_group_weights.csv'
stock_weights_path = folder_path / 'final_portfolio_weights.csv'

df_groups.to_csv(group_weights_path, index=False)
df_betas.to_csv(stock_weights_path, index=False)

print(f"\nPortfolio weights successfully saved in {folder_path}")