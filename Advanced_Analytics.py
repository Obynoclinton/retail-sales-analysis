# Import visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Import necessary libraries
import pandas as pd

# Predict future sales using simple linear regression.
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


# Define the file path
file_path = "C:/Users/HP/Desktop/projects/Retail_Sales_Analysis/Cleaned_Superstore.csv"  # Ensure this path is correct

# Load the dataset with the appropriate encoding
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Dataset information
print("\nDataset Information:")
print(data.info())

# Display dataset info
print("\nDataset Information:")
print(data.info())

# RFM Analysis
import datetime as dt

# Ensure 'order_date' column is in datetime format
data['order_date'] = pd.to_datetime(data['order_date'])

# Define reference date for recency calculation
reference_date = data['order_date'].max() + dt.timedelta(days=1)

# Calculate RFM metrics
rfm = data.groupby('customer_id').agg({
    'order_date': lambda x: (reference_date - x.max()).days,  # Recency
    'order_id': 'count',  # Frequency
    'sales': 'sum'  # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# Add RFM scores (1 to 5 scale for each metric)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'], 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

# Combine scores into an RFM score
rfm['RFM_Score'] = rfm['R_Score'].astype(int) + rfm['F_Score'].astype(int) + rfm['M_Score'].astype(int)

print("\nRFM Analysis Results:")
print(rfm.head())

# Visualize the distribution of RFM scores
sns.histplot(rfm['RFM_Score'], bins=10, kde=False, color='blue')
plt.title('Distribution of RFM Scores')
plt.xlabel('RFM Score')
plt.ylabel('Number of Customers')
plt.show()


# Prepare data for regression
if 'order_date' in data.columns and 'sales' in data.columns:
    data['order_month'] = data['order_date'].dt.month
    data['order_year'] = data['order_date'].dt.year

    regression_data = data.groupby(['order_year', 'order_month'])['sales'].sum().reset_index()
    regression_data['time_index'] = range(1, len(regression_data) + 1)

    # Define features and target
    X = regression_data[['time_index']]
    y = regression_data['sales']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\nLinear Regression Results:")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared: {r2:.2f}")

    # Plot actual vs predicted sales
    plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
    plt.title('Actual vs Predicted Sales')
    plt.xlabel('Actual Sales')
    plt.ylabel('Predicted Sales')
    plt.show()


# Using boxplots for outlier detection
numerical_columns = ['sales', 'profit']

for col in numerical_columns:
    sns.boxplot(data[col])
    plt.title(f'Boxplot of {col}')
    plt.show()

# Statistical approach for detecting outliers (Z-scores)
from scipy.stats import zscore

if 'sales' in data.columns:
    data['sales_zscore'] = zscore(data['sales'])
    outliers = data[data['sales_zscore'].abs() > 3]
    print("\nOutliers in Sales:")
    print(outliers)

plt.savefig('filename.png')
rfm.to_csv('rfm_analysis_results.csv', index=False)
