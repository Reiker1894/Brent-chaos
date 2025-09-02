import pandas as pd, numpy as np, json, joblib, os
from data import download_brent, make_returns, DATA_PROC
from chaos import hurst_rs, bds_test, lyapunov_rosenstein
from features import build_supervised
from models import train_rf

os.makedirs(DATA_PROC, exist_ok=True)

def run_pipeline():
    price = download_brent()
    df = make_returns(price)

    # métricas de caos (usa retornos para BDS y Lyapunov; Hurst en precios)
    H = hurst_rs(price['adj_close'].values)
    bds = bds_test(df['ret'].values, m=2)
    lce = lyapunov_rosenstein(df['ret'].values)

    chaos = {"hurst": float(H), "bds_stat": float(bds["stat"]), "bds_p": float(bds["pvalue"]), "lyapunov": float(lce)}
    with open(f"{DATA_PROC}/chaos.json", "w") as f: json.dump(chaos, f, indent=2)

    # dataset supervisado
    idx, X, y, scaler = build_supervised(df, target_col="ret", lags=10)
    model, cv = train_rf(X, y)

    joblib.dump(model, f"{DATA_PROC}/rf_model.joblib")
    joblib.dump(scaler, f"{DATA_PROC}/scaler.joblib")

    # últimos pred
    last_pred = model.predict(X[-1:].copy())[0]
    pd.DataFrame({
      "date":[idx[-1]],
      "ret_pred_next":[last_pred],
    }).to_csv(f"{DATA_PROC}/last_prediction.csv", index=False)

    return chaos, cv, last_pred

if __name__ == "__main__":
    chaos, cv, last_pred = run_pipeline()
    print("Chaos:", chaos)
    print("CV:", cv)
    print("Next ret pred:", last_pred)
