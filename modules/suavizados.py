# modules/suavizados.py

import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

@st.cache_data
def cargar_datos():
    data = yf.download("BZ=F", start="1990-01-01")
    data = data[['Adj Close']].rename(columns={'Adj Close': 'Brent_Price'})
    data.dropna(inplace=True)
    return data

def mostrar_suavizados():
    st.header("Suavizado de la Serie Histórica del Brent")
    df = cargar_datos()

    df['MA_5'] = df['Brent_Price'].rolling(window=5).mean()
    df['MA_22'] = df['Brent_Price'].rolling(window=22).mean()

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df.index, df['Brent_Price'], label="Original", color='gray', linewidth=1)
    ax.plot(df.index, df['MA_5'], label="Media Móvil (5 días)", color='blue')
    ax.plot(df.index, df['MA_22'], label="Media Móvil (22 días)", color='red')
    ax.set_title("Serie diaria del Brent con suavizados")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio (USD)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("""
    **Interpretación sugerida:**
    - La serie original muestra alta volatilidad y ruido a corto plazo.
    - El suavizado de 5 días permite ver tendencias semanales.
    - El de 22 días revela patrones mensuales.
    - La consistencia entre escalas sugiere autosimilitud estructural.
    """)

