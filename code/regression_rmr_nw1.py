import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Step 2: Define the regression model function
def regression_model(x, a, b):
    return a * x + b

df_original = pd.read_csv("data_rmr/shannon_index_scenic_category_nw1.tsv", sep="\t")


df_reshaped = pd.DataFrame()

for idx, row in df_original.iterrows():
    votes = list(map(int, row['votes'].split(',')))
    for vote in votes:
        new_row = row.copy()
        new_row['vote'] = vote
        df_reshaped = pd.concat([df_reshaped, pd.DataFrame([new_row])])

# Drop the original 'votes' column
df_reshaped = df_reshaped.drop(columns=['votes'])
print(df_reshaped.head())

df_reshaped = pd.get_dummies(df_reshaped, columns=['category'], drop_first=True)

# Fit a mixed-effects model with 'shannon', 'count', 'rate', 'variance', and dummy variables for 'category'
# formula = 'vote ~ shannon + count + rate + variance + category_PastureLand + category_Farmland + ...'


# Reshaped DataFrame df_reshaped

# Fit a mixed-effects model using only 'shannon' and 'count'
# formula = 'vote ~ scaled_shannon + count + variance + category'
# formula = 'vote ~ scaled_shannon + count + variance'
# formula = 'vote ~ scaled_shannon + count'
formula = 'vote ~ density + average_clustering + local_efficiency + global_efficiency + conn'


model = smf.mixedlm(formula, df_reshaped, groups=df_reshaped['idx'])
result = model.fit()

# Print summary statistics
print(result.summary())


# p_shannon = result.pvalues['scaled_shannon']
# p_count = result.pvalues['count']

# # Check significance
# if p_shannon < 0.05:
#     print("The effect of 'shannon' is statistically significant.")
# else:
#     print("The effect of 'shannon' is not statistically significant.")

# if p_count < 0.05:
#     print("The effect of 'count' is statistically significant.")
# else:
#     print("The effect of 'count' is not statistically significant.")