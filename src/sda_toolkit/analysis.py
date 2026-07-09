# """
# analysis.py — Exploratory Analysis Module (Hour 8-11)

# TODO (Hour 8-11):
# - summary_stats(df) -> pd.DataFrame      # describe(), dtypes, nulls
# - correlation_matrix(df) -> pd.DataFrame
# - value_counts_report(df, columns=None) -> dict
# - detect_outliers(df, method="iqr"|"zscore") -> dict
# """

#Descriptive statistics of the dataset and returns it as a dataframe

def summary_stats(df):
    stats = df.describe()
    print(f'Data as follow: {stats}')
    return stats


#find the correlation matrix of the dataset and returns it as a dataframe

def correlation_matrix(df):
    corr_matrix = df.corr(numeric_only=True)
    print(f'correlation matrix as follow:{corr_matrix}')
    return corr_matrix


#counts the values of each column in the dataset and returns a dictionary with the counts

def value_counts_report(df):
    results = {}
    for col in df.columns:
        results[col] = df[col].value_counts()
        print(f'{col}')
        print(results[col])
    return results


#removers the extreme values from the dataset using the IQR method

def detect_outliers(df):
    outliers = {}
    for col in df.select_dtypes(include='number').columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q3 - 1.5*iqr
        upper = q3 + 1.5*iqr
        outliers[col] = len(df[(df[col] < lower) | (df[col] > upper)])
    print(f'outliers as follow: {outliers}')
    return outliers

