# converter.py
import pandas as pd

class NevadaConverter:
    """
    Converts raw sales and returns data into Nevada chart format.
    """

    def __init__(self, sale_col='sale_period', return_col='return_period', quantity_col='quantity', time_bucket=None):
        """
        Initialize converter settings.

        Args:
            sale_col (str): Column name for sale period.
            return_col (str): Column name for return period.
            quantity_col (str): Column name for quantity.
            time_bucket (str): Optional time bucketing (e.g., 'M' for month, 'Q' for quarter).
        """
        self.sale_col = sale_col
        self.return_col = return_col
        self.quantity_col = quantity_col
        self.time_bucket = time_bucket

    def _apply_time_bucketing(self, df):
        if self.time_bucket:
            df[self.sale_col] = pd.to_datetime(df[self.sale_col]).dt.to_period(self.time_bucket)
            df[self.return_col] = pd.to_datetime(df[self.return_col]).dt.to_period(self.time_bucket)
        return df

    def to_nevada_format(self, df):
        """
        Converts the DataFrame to Nevada chart format.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: Nevada chart formatted DataFrame.
        """
        df = self._apply_time_bucketing(df)
        pivot = df.pivot_table(
            index=self.sale_col,
            columns=self.return_col,
            values=self.quantity_col,
            aggfunc='sum',
            fill_value=0
        )
        return pivot
