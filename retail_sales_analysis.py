# Import necessary libraries
import pandas as pd

# Define the file path
file_path = "C:/Users/HP/Desktop/projects/Retail_Sales_Analysis/Sample - Superstore.csv"  # Ensure this path is correct

# Load the dataset with the appropriate encoding
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Dataset information
print("\nDataset Information:")
print(data.info())

# Check for missing values
print("\nMissing Values:")
print(data.isnull().sum())

# Statistical summary
print("\nStatistical Summary:")
print(data.describe())


# Preview the dataset
print("Dataset Preview:")
print(data.head())

# Check for missing values
print("\nMissing Values Before Cleaning:")
print(data.isnull().sum())

# Drop rows with all values missing (optional)
data = data.dropna(how='all')

# Fill or drop missing values for specific columns (example)
# Replace NaN in 'Postal Code' with a placeholder
if 'Postal Code' in data.columns:
    data['Postal Code'] = data['Postal Code'].fillna('Unknown')

# Confirm missing values are handled
print("\nMissing Values After Cleaning:")
print(data.isnull().sum())

# Check for duplicate rows
print("\nNumber of Duplicate Rows:", data.duplicated().sum())

# Drop duplicate rows
data = data.drop_duplicates()

# Confirm no duplicates remain
print("\nNumber of Duplicate Rows After Cleaning:", data.duplicated().sum())

# Standardize column names (e.g., make them lowercase, replace spaces with underscores)
data.columns = data.columns.str.lower().str.replace(' ', '_')

# Preview the updated column names
print("\nUpdated Column Names:")
print(data.columns)

# Convert 'order_date' and 'ship_date' to datetime (if present)
if 'order_date' in data.columns and 'ship_date' in data.columns:
    data['order_date'] = pd.to_datetime(data['order_date'])
    data['ship_date'] = pd.to_datetime(data['ship_date'])

# Convert 'sales' and 'profit' to numeric (if necessary)
if 'sales' in data.columns and 'profit' in data.columns:
    data['sales'] = pd.to_numeric(data['sales'], errors='coerce')
    data['profit'] = pd.to_numeric(data['profit'], errors='coerce')

# Create 'shipping_duration' column
if 'order_date' in data.columns and 'ship_date' in data.columns:
    data['shipping_duration'] = (data['ship_date'] - data['order_date']).dt.days

# Extract year and month from 'order_date'
if 'order_date' in data.columns:
    data['order_year'] = data['order_date'].dt.year
    data['order_month'] = data['order_date'].dt.month

# Save the cleaned dataset to a new file
cleaned_file_path = "Cleaned_Superstore.csv"
data.to_csv(cleaned_file_path, index=False)

print(f"\nCleaned dataset saved to {cleaned_file_path}")
