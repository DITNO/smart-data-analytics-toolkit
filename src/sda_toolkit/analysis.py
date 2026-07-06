# """
# analysis.py — Exploratory Analysis Module (Hour 8-11)

# TODO (Hour 8-11):
# - summary_stats(df) -> pd.DataFrame      # describe(), dtypes, nulls
# - correlation_matrix(df) -> pd.DataFrame
# - value_counts_report(df, columns=None) -> dict
# - detect_outliers(df, method="iqr"|"zscore") -> dict
# """


def summary_stats(df):
    stats = df.describe()
    print(f'Data as follow: {stats}')
    return stats

def correlation_matrix(df):
    corr_matrix = df.corr(numeric_only=True)
    print(f'correlation matrix as follow:{corr_matrix}')
    return corr_matrix

def value_counts_report(df):
    results = {}
    for col in df.columns:
        results[col] = df[col].value_counts()
        print(f'{col}')
        print(results[col])
    return results

