import pandas as pd
from .utils import calculate_sums_and_ranks

class RankSetSampler:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def rank_by_sum(self):
        """Adds a 'Sum' column and a 'Rank' column sorted in descending order."""
        self.data['Sum'] = self.data.sum(axis=1)
        self.data['Rank'] = self.data['Sum'].rank(ascending=False, method='dense').astype(int)
        return self.data.sort_values(by='Rank')
