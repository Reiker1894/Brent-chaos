import streamlit as st, pandas as pd, json, joblib
from pathlib import Path

PROC = Path("data/processed")

st.set_page_config(page_title="Brent – Caos & ML", layout="wide")
st.title("Pronóstico Brent con medidas de Caos + ML")

# Datos
# Datos
files = sorted(Path("data/raw").glob("brent_*.csv"))
if files:
    latest_file = files[-1]
    price = pd.read_csv(latest_file, index_col=0, parse_dates=True)
else:
    st.error("⚠️ No se encontraron archivos en data/raw/")
    price = pd.DataFrame()

rets  = pd.read_parquet(PROC/"brent_returns.parquet")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Precio Brent")
    st.line_chart(price["adj_close"])
with col2:
    st.subheader("Retornos logarítmicos")
    st.line_chart(rets["ret"])

# Métricas de caos
st.subheader("Medidas de Caos")
chaos = json.load(open(PROC/"chaos.json"))
st.metric("Hurst (precio)", f"{chaos['hurst']:.3f}")
st.metric("Lyapunov (retornos)", f"{chaos['lyapunov']:.4f}")
st.metric("BDS p-valor (retornos)", f"{chaos['bds_p']:.4f}")

# Predicción próxima vela (retorno)
last_pred = pd.read_csv(PROC/"last_prediction.csv")
st.subheader("Predicción próxima variación (retorno)")
st.write(last_pred)
st.caption("Modelo: RandomForest con lags de retornos. Próximo paso: incluir features de caos en el vector X.")
