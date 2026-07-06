# """
# cleaning.py — Data Cleaning Module (Hour 5-8)

# TODO (Hour 5-8):
# - drop_duplicates(df) -> pd.DataFrame
# - handle_missing(df, strategy="mean"|"median"|"drop"|"fill") -> pd.DataFrame
# - fix_dtypes(df) -> pd.DataFrame
# - cleaning_report(df_before, df_after) -> dict   # summary of what changed
# """

from turtle import pd
import pandas as pd


def drop_duplicates(df):
    # count before
    before_count = len(df)
    # drop duplicates
    df_cleaned = df.drop_duplicates()
    # count after
    after_count = len(df_cleaned)
    # print how many were removed
    print(f"No. of duplicate rows removed: {before_count - after_count}")
    # return cleaned df
    return df_cleaned

def handle_missing(df, strategy="mean"):

    print(df.isnull().sum().sum(), "missing values before cleaning")

    if strategy == "drop":
        df_cleaned = df.dropna()
    elif strategy == "mean":
        df_cleaned = df.fillna(df.mean(numeric_only = True))
    elif strategy == "median":
        df_cleaned = df.fillna(df.median(numeric_only = True))
    elif strategy == "fill":
        df_cleaned = df.fillna(0)
    else:
        print(f"unknown stategy: {strategy}. no changes made.")
        return df_cleaned

    return df_cleaned

def fix_dtype(df):
    # convert object columns to string
    for col in df:
        df[col] = pd.to_numeric(df[col],errors='ignore')
    
    print("Data types after cleaning:")
    print(df.dtypes)
    return df

