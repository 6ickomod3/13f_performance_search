import re
import pandas as pd

# Specify the path to your Excel file
xlsx_file = '/Users/jdai/Documents/13f/data/performance_all.xlsx'

# Read the Excel file into a Pandas DataFrame
# The sheet_name parameter specifies the name of the sheet to read ('Rebalancing' in this case)
df = pd.read_excel(xlsx_file, sheet_name='Rebalancing')

# Now, 'df' is a Pandas DataFrame containing the data from the "Rebalancing" sheet
# You can work with the data using Pandas DataFrame operations
# For example, you can print the first few rows of the DataFrame:

# Define a regular expression pattern for matching "yyyy-mm-dd" format
date_pattern = r'\d{4}-\d{2}-\d{2}'

# Find 
for row_id in df.shape[0]:
    content = str(df.iloc[row_id,0])

    # Use re.search() to find the date pattern in the string
    match = re.search(date_pattern, content)

    # Check if a match was found
    if match:
        # Extract the matched date
        matched_date = match.group()
        print("Date found:", matched_date)