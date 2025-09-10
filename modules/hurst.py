# modules/hurst.py

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from hurst import compute_Hc

@st.cache_data
def cargar_datos():
    data = yf.download("BZ=F", start="1990-01-01")
    data = data[['Adj Close']].rename(columns={'Adj Close': 'Brent_Price'})
    data.dropna(inplace=True)
    return data

def mostrar_exponente_hurst():
    st.header("Cálculo del Exponente de Hurst")
    df = cargar_datos()

    fecha_inicio = st.date_input("Fecha de inicio", df.index.min().date(), key='h_inicio')
    fecha_fin = st.date_input("Fecha de fin", df.index.max().date(), key='h_fin')

    if fecha_inicio >= fecha_fin:
        st.error("La fecha de inicio debe ser anterior a la fecha de fin.")
        return

    df_filtrado = df[(df.index >= pd.to_datetime(fecha_inicio)) & (df.index <= pd.to_datetime(fecha_fin))]
    if df_filtrado.empty:
        st.warning("No hay datos para el rango seleccionado.")
        return

    ts = df_filtrado['Brent_Price'].values
    H, c, data = compute_Hc(ts, kind='price', simplified=True)

    st.subheader("Resultado del Exponente de Hurst")
    st.write(f"**H = {H:.4f}**")

    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(data[0], c * data[0]**H, label=f"Ajuste H = {H:.4f}", color='red')
    ax.scatter(data[0], data[1], alpha=0.6)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("Escala (log)")
    ax.set_ylabel("Desviación estándar (log)")
    ax.set_title("Estimación del Exponente de Hurst")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("""
    **Interpretación sugerida:**
    - Si **H > 0.5**, hay persistencia: tendencias tienden a continuar (memory effect).
    - Si **H < 0.5**, hay anti-persistencia: reversión frecuente a la media.
    - Si **H ≈ 0.5**, comportamiento tipo paseo aleatorio.
    - Este análisis ayuda a decidir si modelos como ARIMA, LSTM o fractales pueden capturar mejor la dinámica del Brent.
    """)
