# """
# cleaning.py — Data Cleaning Module (Hour 5-8)
#
# Functions to clean pandas DataFrames:
#   - drop_duplicates()   — removes exact duplicate rows
#   - handle_missing()    — fills or drops NaN values
#   - fix_dtype()         — converts string-looking columns to numbers
# """

import pandas as pd
# FIX: Removed bogus `from turtle import pd` — this was a copy-paste
# error that imported the turtle graphics module instead of pandas.


def drop_duplicates(df):
    """
    Remove exact duplicate rows from the DataFrame.

    Uses pandas' drop_duplicates() which keeps the first occurrence.
    Prints how many rows were removed for user feedback.
    """
    before_count = len(df)
    df_cleaned = df.drop_duplicates()
    after_count = len(df_cleaned)
    print(f"No. of duplicate rows removed: {before_count - after_count}")
    return df_cleaned


def handle_missing(df, strategy="mean"):
    """
    Handle missing (NaN) values in the DataFrame.

    Strategies:
      - "mean"   : fills numeric NaNs with column mean
      - "median" : fills numeric NaNs with column median
      - "drop"   : removes any row containing a NaN
      - "fill"   : fills ALL NaNs with 0

    FIX: The `else` branch originally had `return df_cleaned` but
    `df_cleaned` was never assigned in that path (NameError at
    runtime). Changed to `return df` so unknown strategies return
    the original DataFrame unchanged.
    """
    print(df.isnull().sum().sum(), "missing values before cleaning")

    if strategy == "drop":
        df_cleaned = df.dropna()
    elif strategy == "mean":
        df_cleaned = df.fillna(df.mean(numeric_only=True))
    elif strategy == "median":
        df_cleaned = df.fillna(df.median(numeric_only=True))
    elif strategy == "fill":
        df_cleaned = df.fillna(0)
    else:
        print(f"unknown strategy: {strategy}. no changes made.")
        return df  # FIXED: was `return df_cleaned` (unbound variable)

    return df_cleaned


def fix_dtype(df):
    """
    Attempt to convert string columns into numeric columns.

    Only targets object/str columns. Uses pd.to_numeric() with
    errors='coerce' (invalid values become NaN). If at least 50%
    of values successfully convert, the column is replaced with
    the numeric version.

    FIX: The original code ran `pd.to_numeric(df[col], errors='ignore')`
    on ALL columns (including already-numeric ones). With 'ignore',
    non-convertible columns are returned unchanged and nothing is
    assigned back — making the entire function a no-op. The fix:
    1. Only inspect object/str columns (skip numbers)
    2. Use 'coerce' to actually attempt conversion
    3. Use a 50% threshold to avoid clobbering text columns
    4. Actually assign the result back to the column
    """
    for col in df.select_dtypes(include=["object", "str"]).columns:
        converted = pd.to_numeric(df[col], errors="coerce")
        # Only keep numeric conversion if at least half the values converted
        if converted.notna().sum() >= len(converted) * 0.5:
            df[col] = converted

    print("Data types after cleaning:")
    print(df.dtypes)
    return df

