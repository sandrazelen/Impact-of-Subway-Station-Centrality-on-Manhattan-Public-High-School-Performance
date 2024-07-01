import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from scipy.stats import shapiro, anderson
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt

def main():
  filename = f"C:/Users/carol/Downloads/perfomance_centrality_dataset_final - perfomance_centrality_dataset2.csv"
  df = pd.read_csv(filename)
  # print(df)
  cor_matrix = df.corr()
  # print(cor_matrix)

  X = df.drop(columns=['Student Achievement', 'Rigorous Instruction', 'Collaborative Teachers', 'Supportive Environment', 'Effective School Leadership', 'Strong Family-Community Ties', 'Trust'])
  y = df['Student Achievement']

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

  model = LinearRegression()
  model.fit(X_train, y_train)

  print("Coefficients: ", model.coef_)
  print("Intercept: ", model.intercept_)

  summary = df.describe(include="all")
  # print(summary)

  y_pred = model.predict(X_test)
  print("Predictions: ", y_pred)
  plt.figure(figsize=(10, 6))
  plt.scatter(np.arange(len(y_test)), y_test, color='blue', label='Actual', alpha=0.3)
  plt.scatter(np.arange(len(y_test)), y_pred, color='red', label='Predicted', alpha=0.3)

  plt.plot(np.arange(len(y_test)), y_test, color='blue', alpha=0.5)
  plt.plot(np.arange(len(y_test)), y_pred, color='red', alpha=0.5)
  
  plt.title('Actual vs Predicted')
  plt.xlabel('Observations')
  plt.ylabel('Student Achievement')
  plt.legend()
  # plt.show()

  residuals = y_test - y_pred
  print('\nTests for Student Achievement\n')
  bp_test = het_breuschpagan(residuals, X_test)
  print("Breusch-Pagan Statistic:", bp_test[0])
  print("Breusch-Pagan p-value:", bp_test[1])

  # Autocorrelation check: Durbin Watson test
  dw_test = durbin_watson(residuals)
  print("Durbin-Watson Statistic:", dw_test)

  # Normality of residuals check: Shapiro-Wilk and Anderson-Darling tests
  shapiro_test = shapiro(residuals)
  print("Shapiro-Wilk Test p-value:", shapiro_test[1])
  anderson_test = anderson(residuals, dist='norm')
  print("Anderson-Darling Test Statistic:", anderson_test.statistic)
  # print("Anderson-Darling Critical Values:", anderson_test.critical_values)
  print("Anderson-Darling Significance Levels:", anderson_test.significance_level)

  print("\nMulticollinearity (Variance Inflation Factor - VIF):")
  vif_data = pd.DataFrame()
  vif_data["feature"] = X.columns
  vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
  print(vif_data)


if __name__ == "__main__":
    main()