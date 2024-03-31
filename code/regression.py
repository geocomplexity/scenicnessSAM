import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import statsmodels.api as sm


# Step 2: Define the regression model function
def regression_model(x, a, b):
    return a * x + b

df = pd.read_csv("data/shannon_index_scenic_category.tsv", sep="\t")

# Step 3: Extract the data from the DataFrame
x = df['scaled_shannon'].values
y = df['rate'].values
y_uncertainty = df['variance'].values

# Step 4: Perform curve fitting using curve_fit
# Set a large weight for data points with zero uncertainty
y_uncertainty = np.where(y_uncertainty != 0, 1.0 / y_uncertainty, 0)
# y_uncertainty = np.where(y_uncertainty != 0, y_uncertainty, 0)

# Mask the weights for data points with non-zero uncertainty
# weights_non_zero_uncertainty = np.where(y_uncertainty != 0, weights, 0)

# Perform the curve fitting
params, covariance_matrix = curve_fit(regression_model, x, y, sigma=y_uncertainty, absolute_sigma=True)

# Retrieve the fitted parameters and their uncertainties
fitted_a, fitted_b = params
uncertainties_a = np.sqrt(covariance_matrix[0, 0])
uncertainties_b = np.sqrt(covariance_matrix[1, 1])

# Step 5: Print the fitted parameters and their uncertainties
print(f"Fitted 'a' parameter: {fitted_a:.4f} +/- {uncertainties_a:.4f}")
print(f"Fitted 'b' parameter: {fitted_b:.4f} +/- {uncertainties_b:.4f}")

# Step 6: Calculate and print fit statistics
y_pred = regression_model(x, fitted_a, fitted_b)

# Mean Squared Error (MSE)
mse = np.mean((y - y_pred)**2)
print(f"Mean Squared Error (MSE): {mse:.4f}")

# Root Mean Squared Error (RMSE)
rmse = np.sqrt(mse)
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

# Coefficient of Determination (R-squared)
total_variation = np.sum((y - np.mean(y))**2)
explained_variation = np.sum((y_pred - np.mean(y))**2)
r_squared = explained_variation / total_variation
print(f"Coefficient of Determination (R-squared): {r_squared:.4f}")


# Step 5: Visualize the regression line and data
plt.errorbar(x, y, y_uncertainty, fmt='*', label='Data with uncertainty')
plt.plot(x, regression_model(x, fitted_a, fitted_b), label='Fitted Line')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
# plt.show()
plt.show()


# # Remove rows with NaN values
# df = df.dropna()

# # Make sure y_std values are not zero
# df = df[df['std'] != 0]

# # # Add a constant column for the intercept term in the regression
# # data_with_intercept = sm.add_constant(df['scaled_shannon'])

# # # Perform the WLS regression
# # wls_model = sm.WLS(df['rate'], data_with_intercept, weights=1 / df['std']**2)
# # results = wls_model.fit()

# # # Print the regression summary
# # print(results.summary())

# results_by_category = {}
# for cat in df['category'].unique():
#     data_category = df[df['category'] == cat]
#     data_with_intercept = sm.add_constant(data_category['scaled_shannon'])
#     wls_model = sm.WLS(data_category['rate'], data_with_intercept, weights=1 / data_category['std']**2)
#     results = wls_model.fit()
#     results_by_category[cat] = results
#     print(results.summary())

# # Print the regression summaries for each category
# for cat, results in results_by_category.items():
#     print(f"Regression results for category {cat}:")
#     print(results.summary())