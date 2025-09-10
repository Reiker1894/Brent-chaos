# modules/estadistica.py

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

@st.cache_data
def cargar_datos():
    data = yf.download("BZ=F", start="1990-01-01")
    data = data[['Adj Close']].rename(columns={'Adj Close': 'Brent_Price'})
    data.dropna(inplace=True)
    return data

def mostrar_estadisticas():
    st.header("Estadística Descriptiva del Precio del Brent")
    df = cargar_datos()
    st.markdown("""
    Selecciona el rango de fechas para calcular estadísticas y visualizar la distribución:
    """)

    fecha_inicio = st.date_input("Fecha de inicio", df.index.min().date())
    fecha_fin = st.date_input("Fecha de fin", df.index.max().date())

    if fecha_inicio >= fecha_fin:
        st.error("La fecha de inicio debe ser anterior a la fecha de fin.")
        return

    df_filtrado = df[(df.index >= pd.to_datetime(fecha_inicio)) & (df.index <= pd.to_datetime(fecha_fin))]

    if df_filtrado.empty:
        st.warning("No hay datos para el rango seleccionado.")
        return

    st.subheader("Resumen estadístico")
    resumen = {
        "Media": df_filtrado['Brent_Price'].mean(),
        "Desviación Estándar": df_filtrado['Brent_Price'].std(),
        "Asimetría": skew(df_filtrado['Brent_Price']),
        "Curtosis": kurtosis(df_filtrado['Brent_Price'], fisher=True)
    }
    st.table(pd.DataFrame(resumen, index=["Estadísticas"]))

    st.subheader("Distribución del Precio del Brent")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.histplot(df_filtrado['Brent_Price'], kde=True, stat="density", bins=50, ax=ax, color="skyblue")
    ax.set_title("Histograma con curva de densidad")
    ax.set_xlabel("Precio (USD)")
    ax.set_ylabel("Densidad")
    st.pyplot(fig)

    st.markdown("""
    **Interpretación sugerida:**
    - La **asimetría positiva** indica una cola más larga hacia precios altos.
    - La **curtosis mayor a 3** (distribución leptocórtica) sugiere mayor presencia de eventos extremos.
    - Estas características refuerzan la necesidad de modelos no lineales y robustos.
    """)

