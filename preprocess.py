import pandas as pd

# Load CSV
df = pd.read_csv("data/Pharma_sales.csv")

# Fix column names
df = df.rename(columns={
    "datum": "DATE_ID",
    "Weekday Name": "WEEKDAY"
})

# Drug columns
drug_columns = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']

# Convert wide → long (SALES table)
sales_df = df.melt(
    id_vars=["DATE_ID"],
    value_vars=drug_columns,
    var_name="DRUG_CODE",
    value_name="UNITS_SOLD"
)

# Save output
sales_df.to_csv("data/sales.csv", index=False)

print("Sales data processed:")

# TIME_PERIOD table
time_df = df[["DATE_ID", "Year", "Month", "Hour", "WEEKDAY"]].drop_duplicates()
time_df.to_csv("data/time_period.csv", index=False)

# DRUG_CATEGORY table
drug_codes = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']

drug_df = pd.DataFrame({
    "DRUG_CODE": drug_codes,
    "DESCRIPTION": drug_codes,
    "MFR_ID": [1]*len(drug_codes)
})

drug_df.to_csv("data/drug_category.csv", index=False)

print("All CSVs created")