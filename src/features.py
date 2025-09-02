import pandas as pd
from sklearn.preprocessing import StandardScaler

def build_supervised(df, target_col="ret", lags=5):
    out = df.copy()
    for L in range(1, lags+1):
        out[f"{target_col}_lag{L}"] = out[target_col].shift(L)
    out["y"] = out[target_col].shift(-1)
    out = out.dropna()
    X = out.filter(like=f"{target_col}_lag").values
    y = out["y"].values
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)
    return out.index, Xs, y, scaler
