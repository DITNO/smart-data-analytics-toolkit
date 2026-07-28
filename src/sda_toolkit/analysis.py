# """
# analysis.py — Exploratory Analysis Module (Hour 8-11)
#
# Provides statistical analysis functions for pandas DataFrames:
#   - summary_stats()      -> DataFrame with describe() output
#   - correlation_matrix() -> DataFrame of pairwise correlations
#   - value_counts_report() -> dict of {col: value_counts Series}
#   - detect_outliers()    -> dict of {col: outlier_count} via IQR
# """

import pandas as pd


def summary_stats(df):
    """
    Compute summary statistics for numeric columns.

    Returns df.describe() as a DataFrame. If the input is empty
    (no rows or no columns), returns an empty DataFrame instead
    of crashing (df.describe() raises ValueError on empty input).

    FIX: Added empty-df guard after discovering that calling
    describe() on an empty DataFrame raises a ValueError.
    """
    if df.empty or df.shape[1] == 0:
        print("DataFrame is empty — no statistics to report.")
        return pd.DataFrame()
    stats = df.describe()
    print(f'Summary statistics:\n{stats}')
    return stats


def correlation_matrix(df):
    """
    Compute pairwise correlation of numeric columns.

    Returns a square DataFrame where each cell [i][j] is the
    Pearson correlation coefficient between column i and column j.
    Diagonal is always 1.0 (perfect self-correlation).
    """
    corr_matrix = df.corr(numeric_only=True)
    print(f'correlation matrix as follow:{corr_matrix}')
    return corr_matrix


def value_counts_report(df):
    """
    Count occurrences of each value in every column.

    Returns a dict keyed by column name, where each value is a
    pandas Series from value_counts() (index = unique values,
    values = occurrence counts). Useful for spotting class
    imbalances or categorical distributions.
    """
    results = {}
    for col in df.columns:
        results[col] = df[col].value_counts()
        print(f'{col}')
        print(results[col])
    return results


def detect_outliers(df):
    """
    Detect outliers in numeric columns using the IQR method.

    A value is considered an outlier if it falls below
    Q1 - 1.5*IQR or above Q3 + 1.5*IQR. Returns a dict of
    {column_name: count_of_outliers}.

    FIX: The lower-bound formula was originally `q3 - 1.5*iqr`
    (using Q3 instead of Q1). This meant the lower fence was
    actually above Q3, making it symmetric with the upper fence
    and failing to detect low-side outliers. Corrected to
    `q1 - 1.5*iqr` which is the standard IQR formula.
    """
    outliers = {}
    for col in df.select_dtypes(include='number').columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        # FIXED: was `q3 - 1.5*iqr` — incorrect! Should be `q1 - 1.5*iqr`
        lower = q1 - 1.5*iqr
        upper = q3 + 1.5*iqr
        outliers[col] = len(df[(df[col] < lower) | (df[col] > upper)])
    print(f'outliers as follow: {outliers}')
    return outliers

