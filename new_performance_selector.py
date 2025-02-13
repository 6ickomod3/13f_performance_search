import csv
import sys
import numpy as np
from tabulate import tabulate

# Configuration: list of return columns and required invest style substrings
RETURN_COLUMNS = ['3 Yr Perf Annualized', '5 Yr Perf Annualized', '7 Yr Perf Annualized', '10 Yr Perf Annualized', '3-Year Sortino Equal Weight']
REQUIRED_INVEST_SUBSTRINGS = ['Long-Term Focus']  # Invest style must contain all these substrings
FUND_NAME_COLUMN = 'Filer'
INVEST_STYLE_COLUMN = 'Investing Styles'

def safe_float(x):
    """Try to convert x to float; if not possible, return np.nan."""
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan

if len(sys.argv) < 3:
    print("Usage: python select_funds.py <path_to_csv> <percentile>")
    sys.exit(1)

file_path = sys.argv[1]
TOP_PERCENTILE = float(sys.argv[2])

# Read the CSV file using csv.reader
with open(file_path, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)  # First row is the header

    # Get the index of each required column from the header.
    try:
        fund_name_idx = header.index(FUND_NAME_COLUMN)
        invest_style_idx = header.index(INVEST_STYLE_COLUMN)
    except ValueError as e:
        print("Error: Required column not found in header:", e)
        sys.exit(1)

    return_indices = {}
    for col in RETURN_COLUMNS:
        try:
            return_indices[col] = header.index(col)
        except ValueError:
            print(f"Error: Required return column '{col}' not found in header.")
            sys.exit(1)

    # Read all rows into a list of dictionaries (using header names as keys)
    rows = []
    for row in reader:
        # print(row[-6:])
        # If a row is shorter than expected, fill missing cells with empty strings.
        row_dict = {header[i]: (row[i] if i < len(row) else "") for i in range(42)}
        row_dict.update({f"{INVEST_STYLE_COLUMN}": row[-6]})
        rows.append(row_dict)

# Filter rows: the invest style must contain all required substrings (case-insensitive)
filtered_rows = []
for row in rows:
    invest_style = row.get(f"{INVEST_STYLE_COLUMN}", "")
    if all(s in invest_style for s in REQUIRED_INVEST_SUBSTRINGS):
        filtered_rows.append(row)


# For each return column, compute the 95th percentile among valid (non-NaN) values.
thresholds = {}
for col in RETURN_COLUMNS:
    values = []
    for row in filtered_rows:
        val = safe_float(row.get(col, ""))
        if not np.isnan(val):
            values.append(val)
    thresholds[col] = np.percentile(values, TOP_PERCENTILE) if values else 0

# Now select funds that meet or exceed the threshold in every return column.
top_funds = []
for row in filtered_rows:
    meets_all = True
    for col in RETURN_COLUMNS:
        val = safe_float(row.get(col, ""))
        # Treat NaN as 0
        if np.isnan(val):
            val = 0
        if val < thresholds[col]:
            meets_all = False
            break
    if meets_all:
        top_funds.append(row)

# Prepare the output: only include the fund name, return columns, and invest style.
# output_header = [FUND_NAME_COLUMN] + RETURN_COLUMNS + [INVEST_STYLE_COLUMN]
output_header = [FUND_NAME_COLUMN] + RETURN_COLUMNS
output_data = []
for row in top_funds:
    output_data.append([row.get(col, "") for col in output_header])

# Print the results as a formatted table using tabulate.
print(tabulate(output_data, headers=output_header, tablefmt='psql'))
print("{number_of_filer} filer selected using percentile {percentile}%.".format(number_of_filer=len(output_data),percentile=TOP_PERCENTILE))