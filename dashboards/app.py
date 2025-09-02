import streamlit as st, pandas as pd, json, joblib, sys
from pathlib import Path

# --- Paths
RAW  = Path("data/raw")
PROC = Path("data/processed")
PROC.mkdir(parents=True, exist_ok=True)

# --- Opcional: poder llamar al pipeline si está disponible
sys.path.append("src")
try:
    from pipeline import run_pipeline
except Exception:
    run_pipeline = None  # si no existe, seguimos con fallback

st.set_page_config(page_title="Brent – Caos & ML", layout="wide")
st.title("Pronóstico Brent con medidas de Caos + ML")

# --- Utilidades
def latest_raw_csv() -> Path | None:
    files = sorted(RAW.glob("brent_*.csv"))
    return files[-1] if files else None

@st.cache_data
def load_price() -> pd.DataFrame:
    f = latest_raw_csv()
    if not f:
        raise FileNotFoundError("No hay archivos en data/raw/ con patrón brent_*.csv")
    df = pd.read_csv(f, index_col=0, parse_dates=True)
    if "adj_close" not in df.columns:
        raise ValueError(f"{f} no tiene la columna 'adj_close'")
    return df

@st.cache_data
def load_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    """Carga parquet si existe; si no, lo crea a partir de 'price_df'."""
    fp = PROC / "brent_returns.parquet"
    if fp.exists():
        return pd.read_parquet(fp)
    # crear en caliente
    rets = price_df.copy()
    rets["ret"] = (rets["adj_close"].apply(float).apply(pd.Series).squeeze() if False else
                   (price_df["adj_close"].pipe(pd.Series))).apply(float)
    rets["ret"] = (rets["ret"].apply(pd.to_numeric, errors="coerce")).pipe(pd.Series)
    rets["ret"] = (pd.Series(pd.np.log(price_df["adj_close"])) - pd.Series(pd.np.log(price_df["adj_close"])).shift(1))
    rets = rets[["ret"]].dropna()
    rets.to_parquet(fp)
    return rets

def ensure_pipeline_outputs():
    """Si faltan chaos.json o last_prediction.csv, intenta generarlos con run_pipeline()."""
    need = []
    if not (PROC / "chaos.json").exists(): need.append("chaos.json")
    if not (PROC / "last_prediction.csv").exists(): need.append("last_prediction.csv")
    if need and run_pipeline is not None:
        with st.spinner("Calculando artefactos faltantes (pipeline)…"):
            run_pipeline()
    return need

# --- Botón manual (útil en demo)
colA, colB = st.columns([1,3])
with colA:
    if st.button("🔄 Recalcular ahora", help="Descarga datos, recalcula medidas y modelo"):
        if run_pipeline is None:
            st.warning("No se encontró src/pipeline.py. Usa GitHub Actions o ejecuta el pipeline localmente.")
        else:
            chaos, cv, last_pred = run_pipeline()
            st.success("Listo. Artefactos actualizados.")

# --- Carga de datos
try:
    price = load_price()
except Exception as e:
    st.error(f"⚠️ Precios no disponibles: {e}")
    st.stop()

# returns (crea parquet si falta)
try:
    rets = load_returns(price)
except Exception as e:
    st.error(f"⚠️ No se pudieron construir retornos: {e}")
    st.stop()

# --- Gráficos principales
col1, col2 = st.columns(2)
with col1:
    st.subheader("Precio Brent")
    st.line_chart(price["adj_close"])
with col2:
    st.subheader("Retornos logarítmicos")
    st.line_chart(rets["ret"])

# --- Medidas de caos
st.subheader("Medidas de Caos")
missing = ensure_pipeline_outputs()

# chaos.json con fallback amigable
try:
    chaos = json.load(open(PROC / "chaos.json"))
    st.metric("Hurst (precio)", f"{chaos.get('hurst', float('nan')):.3f}")
    st.metric("Lyapunov (retornos)", f"{chaos.get('lyapunov', float('nan')):.4f}")
    st.metric("BDS p-valor (retornos)", f"{chaos.get('bds_p', float('nan')):.4f}")
except Exception:
    st.warning("No se encontró chaos.json. Ejecuta el pipeline (botón arriba) o el Action de GitHub.")

# --- Predicción próxima vela
st.subheader("Predicción próxima variación (retorno)")
try:
    last_pred = pd.read_csv(PROC / "last_prediction.csv")
    st.write(last_pred)
except Exception:
    st.info("No hay 'last_prediction.csv'. Recalcula con el botón o espera al workflow diario.")

st.caption("Modelo: RandomForest con lags de retornos. Próximo paso: incluir features de caos en X.")
