# modules/suavizados.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
@st.cache_data
def cargar_datos():
    start = "1987-05-20"
    end = "2025-09-07"
    df = web.DataReader("DCOILBRENTEU", "fred", start, end).dropna()
    df = df.rename(columns={"DCOILBRENTEU": "Brent_Price"})
    return df

def mostrar_suavizados():
    st.header("Suavizado de la Serie Histórica del Brent")
    df = cargar_datos()

    # Parámetros interactivos
    dias_semanal = st.slider("Ventana suavizado semanal (días)", 2, 10, 5)
    dias_mensual = st.slider("Ventana suavizado mensual (días)", 10, 30, 22)

    # Calcular medias móviles
    df["MA_semanal"] = df["Brent_Price"].rolling(window=dias_semanal).mean()
    df["MA_mensual"] = df["Brent_Price"].rolling(window=dias_mensual).mean()

    # Mostrar gráfico
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df.index, df["Brent_Price"], label="Original", color='black', alpha=0.4)
    ax.plot(df.index, df["MA_semanal"], label=f"Media Móvil ({dias_semanal} días)", color='blue')
    ax.plot(df.index, df["MA_mensual"], label=f"Media Móvil ({dias_mensual} días)", color='red')
    ax.set_title("Serie diaria del Brent con suavizado semanal y mensual")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio (USD)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("""
    **Interpretación:**
    - Las medias móviles permiten suavizar las oscilaciones diarias del precio.
    - El suavizado mensual (línea roja) muestra mejor las tendencias de largo plazo.
    - El suavizado semanal (línea azul) responde más rápido a cambios recientes.
    """)
