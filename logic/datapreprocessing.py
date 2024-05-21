import pandas as pd

# Load the dataset
df = pd.read_csv('logic\data\megaGymDataset.csv')

# Display the first few rows of the dataframe
print("First few rows of the dataset:")
print(df.head())

# Display the shape of the dataframe
print("\nNumber of rows and columns:")
print(df.shape)

# Count the number of nan values in each column
print("\nCount of null values in each column:")
print(df.isna().sum())

# Display information about the dataframe
print("\nInformation about the dataframe:")
print(df.info())

# Summary statistics for numerical columns
print("\nSummary statistics for numerical columns:")
print(df.describe())


# Count of unique values in each categorical column
print("\nCount of unique values in each categorical column:")
for col in df.select_dtypes(include=['object']).columns:
    print(f"Unique values in {col}: {df[col].nunique()}")

# Display the counts of unique values for each categorical column
print("\nCounts of unique values for each categorical column:")
for col in df.select_dtypes(include=['object']).columns:
    print(f"\nValue counts for column {col}:")
    print(df[col].value_counts())

# Replace NaN values in the 'Desc' column with a specific string
df['Desc'] = df['Desc'].fillna('Description is not given yet')


# Remove the 'Rating' and 'RatingDesc' columns
df = df.drop(columns=['Rating', 'RatingDesc'])

# Count the number of nan values in each column
print("\nCount of null values in each column:")
print(df.isna().sum())

# Save the cleaned dataset to a new CSV file
df.to_csv('logic\data\megaGymDataset_cleaned.csv', index=False)

print("The dataset has been cleaned and saved as 'megaGymDataset_cleaned.csv'.")