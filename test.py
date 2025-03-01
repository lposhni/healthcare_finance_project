import pandas as pd

# Read the data from the CSV file
df = pd.read_csv('output.csv')

# Show the columns to check the exact names
print("Columns in DataFrame:", df.columns)

# Remove duplicates based on 'video_title' and 'video_id', keeping the first occurrence
df_unique = df.drop_duplicates(subset=['video_title', 'video_id'], keep='first')

# Show the cleaned DataFrame
print("\nDataFrame After Removing Duplicates:")
print(df_unique)

# Save the cleaned data back to the CSV file
df_unique.to_csv('output_cleaned.csv', index=False)
