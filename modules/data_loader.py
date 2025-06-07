import pandas as pd
import os

# --- The Single, Global Cleaning Function ---
def clean_arrivals_dataframe(df):
    """
    Cleans an arrivals dataframe robustly. It handles non-string country names,
    removes total rows, and ensures all value columns are numeric.
    """
    if df.empty or 'Country' not in df.columns:
        return pd.DataFrame()

    df = df.copy()

    # Step 1: Force the 'Country' column to be string type. This is crucial.
    df['Country'] = df['Country'].astype(str)

    # Step 2: Filter out rows that are not valid countries ('nan', 'TOTAL', blanks).
    invalid_countries = ['NAN', 'TOTAL']
    df = df[~df['Country'].str.strip().str.upper().isin(invalid_countries)]
    df = df[df['Country'].str.strip() != '']

    # Step 3: Ensure all other columns are cleanly converted to numeric.
    for col in df.columns:
        if col != 'Country':
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    return df

# --- Central Data Loading ---
def safe_read_csv(file_path, **kwargs):
    """Safely reads a CSV with a default thousands separator."""
    try:
        kwargs.setdefault('thousands', ',')
        return pd.read_csv(file_path, **kwargs)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()

# Load and IMMEDIATELY clean each arrivals dataframe.
arrivals_data_raw = {
    '2024': safe_read_csv(os.path.join('data', '2024_arrivals.csv')),
    '2023': safe_read_csv(os.path.join('data', '2023_arrivals.csv')),
    '2022': safe_read_csv(os.path.join('data', '2022_arrivals.csv')),
    '2021': safe_read_csv(os.path.join('data', '2021_arrivals.csv')),
    '2020': safe_read_csv(os.path.join('data', '2020_arrivals.csv')),
    '2019': safe_read_csv(os.path.join('data', '2019_arrivals.csv'))
}

# This is the main dictionary of clean data that all other modules will import and use.
arrivals_data = {year: clean_arrivals_dataframe(df) for year, df in arrivals_data_raw.items()}

# Load purpose of visit data and ensure numeric types
purpose_data_raw = safe_read_csv(os.path.join('data', 'tourism_data_purpose_of_visit.csv'))
purpose_data = purpose_data_raw.copy()
for col in purpose_data.columns:
    if col != 'Country':
        purpose_data[col] = pd.to_numeric(purpose_data[col], errors='coerce').fillna(0)

# The geo_cleaned_data is now a simple reference to the already cleaned arrivals_data.
geo_cleaned_data = arrivals_data

# --- Common Constants ---
COLORS = {
    'primary': '#FF4B2B',
    'secondary': '#009C72',
    'background': '#FFF9F0',
    'text': '#2C3E50'
}