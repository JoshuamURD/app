import pandas as pd

# Load the CSV file (adjust the file path as needed)
csv_path = 'data.csv'

# Read the CSV file
df = pd.read_csv(csv_path, encoding='ISO-8859-1', on_bad_lines='skip', engine='python')

# Select only the columns you're interested in
columns_of_interest = ['drg090', 'hashed_customer', 'ADMISSION_DTE', 'DISCHARGE_DTE', 'POSTCODE_LATEST', 'Age_at_admission']
df_cleaned = df[columns_of_interest].copy()  # Create a copy to avoid SettingWithCopyWarning

# Filter out rows where 'drg090' is missing or NaN
df_cleaned = df_cleaned[df_cleaned['drg090'].notna()]

# Convert 'Age_at_admission' to numeric, forcing errors to NaN and dropping invalid or unrealistic ages
df_cleaned['Age_at_admission'] = pd.to_numeric(df_cleaned['Age_at_admission'], errors='coerce')

# Filter out rows with invalid ages (e.g., NaN, ages less than 12, or greater than 25)
df_cleaned = df_cleaned[(df_cleaned['Age_at_admission'] >= 12) & (df_cleaned['Age_at_admission'] <= 25)]

# Convert the 'hashed_customer' column to unique numbers using pandas factorize
df_cleaned['hashed_customer_number'] = pd.factorize(df_cleaned['hashed_customer'])[0]

# Drop the original 'hashed_customer' column if you don't need it anymore
df_cleaned = df_cleaned.drop(columns=['hashed_customer'])

# Export the cleaned data to a new CSV file
csv_output_path = '../output.csv'
df_cleaned.to_csv(csv_output_path, index=False)

print("Cleaned data with rows where 'drg090' has a value, age between 12 and 25, and hashed_customer converted to unique numbers has been saved to", csv_output_path)
