import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import statsmodels.api as sm


# Step 2: Define the regression model function
def regression_model(x, a, b):
    return a * x + b

# category    density average_clustering  local_efficiency    global_efficiency   conn
df = pd.read_csv("data/shannon_index_scenic_category_nw1.tsv", sep="\t")
# df = pd.read_csv("data/shannon_index_scenic_category3.tsv", sep="\t")
# df = pd.read_csv("data/shannon_index_scenic_category.tsv", sep="\t")


# Step 3: Extract the data from the DataFrame
scaled_shannon = df['scaled_shannon'].values
count = df['count'].values
y = df['rate'].values
y_uncertainty = df['variance'].values
density = df['density'].values
average_clustering = df['average_clustering'].values
local_efficiency = df['local_efficiency'].values
global_efficiency = df['global_efficiency'].values
conn = df['conn'].values


epsilon = 1e-6
weights = np.where(y_uncertainty != 0, 1.0 / y_uncertainty, 1.0 / epsilon)

# X = sm.add_constant(np.column_stack((scaled_shannon, count, density, average_clustering, local_efficiency, global_efficiency, conn)))
X = sm.add_constant(np.column_stack((count, density, average_clustering, local_efficiency, conn)))


# Perform weighted least squares regression
model = sm.WLS(y, X)
# model = sm.WLS(y, X, weights=weights)
results = model.fit()

# Print the regression results
print(results.summary())