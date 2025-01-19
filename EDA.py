# Import visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Import necessary libraries
import pandas as pd

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

# Summary statistics for numerical columns
print("\nSummary Statistics:")
print(data.describe())

# Check unique values in categorical columns
categorical_columns = data.select_dtypes(include=['object']).columns
for col in categorical_columns:
    print(f"\nUnique values in {col}:")
    print(data[col].unique())

# Total sales by category
if 'category' in data.columns and 'sales' in data.columns:
    category_sales = data.groupby('category')['sales'].sum().sort_values(ascending=False)
    print("\nSales by Category:")
    print(category_sales)

    # Plot sales by category
    category_sales.plot(kind='bar', color='skyblue', title='Sales by Category')
    plt.ylabel('Total Sales')
    plt.show()


# Total sales by region
if 'region' in data.columns and 'sales' in data.columns:
    region_sales = data.groupby('region')['sales'].sum().sort_values(ascending=False)
    print("\nSales by Region:")
    print(region_sales)

    # Plot sales by region
    region_sales.plot(kind='bar', color='orange', title='Sales by Region')
    plt.ylabel('Total Sales')
    plt.show()

# Profit distribution
if 'profit' in data.columns:
    sns.histplot(data['profit'], kde=True, color='green', bins=30)
    plt.title('Profit Distribution')
    plt.xlabel('Profit')
    plt.ylabel('Frequency')
    plt.show()

# Shipping duration vs sales
if 'shipping_duration' in data.columns and 'sales' in data.columns:
    sns.scatterplot(x='shipping_duration', y='sales', data=data)
    plt.title('Shipping Duration vs Sales')
    plt.xlabel('Shipping Duration (days)')
    plt.ylabel('Sales')
    plt.show()

# Monthly sales trend
if 'order_month' in data.columns and 'order_year' in data.columns and 'sales' in data.columns:
    monthly_sales = data.groupby(['order_year', 'order_month'])['sales'].sum().reset_index()
    monthly_sales['month_year'] = monthly_sales['order_year'].astype(str) + '-' + monthly_sales['order_month'].astype(str)
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='month_year', y='sales', data=monthly_sales, marker='o')
    plt.xticks(rotation=45)
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month-Year')
    plt.ylabel('Total Sales')
    plt.show()

# Correlation heatmap
numerical_columns = data.select_dtypes(include=['number']).columns
correlation_matrix = data[numerical_columns].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()
