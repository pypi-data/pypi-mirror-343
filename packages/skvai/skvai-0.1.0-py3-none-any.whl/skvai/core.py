# skvai/core.py

import pandas as pd

class CSVData:
    def __init__(self, df: pd.DataFrame, target_column: str = None):
        self.df = df
        self.target_column = target_column

        if target_column:
            if target_column not in df.columns:
                raise ValueError(f"Target column '{target_column}' not found in DataFrame.")
            self.X = df.drop(columns=[target_column])
            self.y = df[target_column]
        else:
            self.X = df
            self.y = None

    @classmethod
    def from_csv(cls, filepath: str, target_column: str = None):
        df = pd.read_csv(filepath)
        return cls(df, target_column)