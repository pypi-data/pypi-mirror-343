import pandas as pd

def calculate_sums_and_ranks(df: pd.DataFrame):
    """Returns a DataFrame with added 'Sum' and 'Rank' columns."""
    df = df.copy()
    df['Sum'] = df.sum(axis=1)
    df['Rank'] = df['Sum'].rank(ascending=False, method='dense').astype(int)
    return df.sort_values(by='Rank')
