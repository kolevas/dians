import pandas as pd
from stock_indicators import Quote


def get_quotes(df):
    return [
        Quote(row.entrydate, None, row['maximumprice'], row['minimumprice'], row['avgprice'], None)
        for _, row in df.iterrows()
        if pd.notnull(row['maximumprice']) and pd.notnull(row['minimumprice']) and pd.notnull(row['avgprice'])
    ]