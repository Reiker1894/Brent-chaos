import os, pandas as pd, numpy as np
from datetime import datetime
import yfinance as yf

DATA_RAW = "data/raw"
DATA_PROC = "data/processed"
os.makedirs(DATA_RAW, exist_ok=True)
os.makedirs(DATA_PROC, exist_ok=True)

def download_brent(start="2010-01-01", end=None, ticker="BZ=F"):
    end = end or datetime.today().strftime("%Y-%m-%d")
    df = yf.download(ticker, start=start, end=end)
    df = df.rename(columns={"Adj Close": "adj_close"})
    df = df[["adj_close"]].dropna()
    df.index.name = "date"
    df.to_csv(f"{DATA_RAW}/brent_{start}_{end}.csv")
    return df

def make_returns(df):
    out = df.copy()
    out["ret"] = np.log(out["adj_close"]).diff()
    out = out.dropna()
    out.to_parquet(f"{DATA_PROC}/brent_returns.parquet")
    return out

if __name__ == "__main__":
    price = download_brent()
    make_returns(price)
