import pandas as pd
import numpy as np
import re

def clean_messy_csv(input_file, output_file):
    print(f"⏳ Loading '{input_file}'...")
    
    # 1. Load the file. 
    # We use 'python' engine just in case the delimiters are mixed up.
    try:
        df = pd.read_csv(input_file, encoding='utf-8', on_bad_lines='warn')
    except UnicodeDecodeError:
        # Fallback for weird Windows encodings
        df = pd.read_csv(input_file, encoding='cp1252', on_bad_lines='warn')
    
    print(f"Original rows: {len(df)}")

    # 2. Clean Column Names
    # Strip spaces, make lowercase, replace spaces with underscores
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    print("✅ Standardized column headers.")

    # 3. Strip Whitespace from all text cells
    # This turns "  John " into "John"
    df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

    # 4. Standardize Missing Values (Nulls)
    # Replace various empty/null representations with actual NaN (Not a Number)
    missing_vals = ['', 'NA', 'N/A', 'null', 'NULL', 'not available', '-', 'none']
    df = df.replace(missing_vals, np.nan)

    # 5. Remove Duplicate Rows
    # (Fixes the duplicate "Dave" row)
    initial_len = len(df)
    df = df.drop_duplicates()
    print(f"✅ Removed {initial_len - len(df)} duplicate rows.")

    # 6. Fix the ID Column
    # Coerce to numbers, drop rows where ID is completely broken (like 'N/A')
    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    df = df.dropna(subset=['id'])
    df['id'] = df['id'].astype(int) # Convert floats back to integers (1.0 -> 1)

    # 7. Fix Salary (e.g., "$70,000" -> 70000)
    if 'salary' in df.columns:
        df['salary'] = df['salary'].astype(str).str.replace(r'[,$]', '', regex=True)
        df['salary'] = pd.to_numeric(df['salary'], errors='coerce')

    # 8. Fix Dates
    # "format='mixed'" tells pandas to figure out the dates even if some are MM/DD and some are YYYY-MM-DD
    if 'join_date' in df.columns:
        df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce', format='mixed')
        # Optional: Standardize the format to YYYY-MM-DD
        df['join_date'] = df['join_date'].dt.strftime('%Y-%m-%d')

    # 9. Fix Names (Handle "Henry;Ford")
    if 'name' in df.columns:
        # Replace semicolons with spaces in names
        df['name'] = df['name'].str.replace(';', ' ', regex=False)
        # Capitalize names properly (e.g., "jane doe" -> "Jane Doe")
        df['name'] = df['name'].str.title()

    # 10. Fix Countries
    if 'country' in df.columns:
        # Uppercase everything, remove periods
        df['country'] = df['country'].str.upper().str.replace('.', '', regex=False)
        # Map specific variations to a standard value
        df['country'] = df['country'].replace({'USA': 'USA', 'US': 'USA'})

    # 11. Clean Emails (Lowercase and Validate)
    if 'email' in df.columns:
        df['email'] = df['email'].str.lower()
        # Regex to check for valid emails. Invalid ones become NaN
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        df.loc[~df['email'].str.match(email_pattern, na=False), 'email'] = np.nan

    # 12. Ensure Age is numeric
    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce')

    # 13. Reset the index 
    df = df.reset_index(drop=True)

    # 14. Save to a new clean file
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"🎉 Success! Clean data saved to '{output_file}'")
    print(f"Cleaned rows: {len(df)}")

    return df

# --- RUN THE SCRIPT ---
if __name__ == "__main__":
    # Make sure 'messy.csv' is exactly the name of your input file
    # (If your file is actually named 'messy.csv.txt', change it below!)
    INPUT = 'messy.csv' 
    OUTPUT = 'clean_data.csv'
    
    cleaned_df = clean_messy_csv(INPUT, OUTPUT)
    
    # Print the first 5 rows to the terminal to see the result
    print("\nPreview of cleaned data:")
    print(cleaned_df.head())