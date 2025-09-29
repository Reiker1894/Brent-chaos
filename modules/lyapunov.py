import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web

@st.cache_data
def cargar_datos():
    start = "1987-05-20"
    end = "2025-09-07"
    df = web.DataReader("DCOILBRENTEU", "fred", start, end).dropna()
    df = df.rename(columns={"DCOILBRENTEU": "Brent_Price"})
    return df

def calcular_lyapunov_series(serie, lag=1, eps=1e-6):
    n = len(serie)
    lyapunov_sum = 0
    count = 0
    log_diffs = []

    for i in range(n - lag):
        diff = serie[i + lag] - serie[i]
        if abs(diff) > eps:
            log_diff = np.log(abs(diff))
            lyapunov_sum += log_diff
            log_diffs.append(log_diff)
            count += 1
        else:
            log_diffs.append(0)

    if count == 0:
        return np.nan, [], []

    return lyapunov_sum / count, log_diffs, list(range(n - lag))

def mostrar_lyapunov():
    st.header("Exponentes de Lyapunov")

    st.markdown("""
    El exponente de **Lyapunov** mide la sensibilidad a las condiciones iniciales en sistemas dinámicos:
    
    - **Positivo** → comportamiento **caótico**.
    - **Cero** → sistema **neutro**.
    - **Negativo** → sistema **estable**.
    
    Su estimación sugiere si hay **dinámica no lineal compleja** en el sistema de precios.
    """)

    df = cargar_datos()
    serie = df["Brent_Price"].dropna().values

    lyap, divergencias, indices = calcular_lyapunov_series(serie)

    st.subheader("Resultado del Exponente")
    st.metric("Lyapunov estimado", f"{lyap:.6f}" if lyap is not None else "NaN")

    st.markdown("""
    - Un **valor positivo** indica evidencia potencial de caos determinista.  
    - Un **valor cercano a cero** puede deberse a ruido o sistemas neutrales.  
    - Esta métrica se recomienda usar con otras pruebas de no linealidad.
    """)

    if divergencias:
        st.subheader("Visualización de divergencias")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(indices, divergencias, label="log(|Δxₜ|)", alpha=0.7)
        ax.set_title("Divergencias entre trayectorias vecinas")
        ax.set_xlabel("Índice")
        ax.set_ylabel("log(|Δxₜ|)")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)


    lyap, divergencias = calcular_lyapunov_series(serie)

    st.subheader("Resultado del Exponente")
    st.metric("Lyapunov estimado", f"{lyap:.6f}")

    st.markdown("""
    - Un **valor positivo** indica evidencia potencial de caos determinista.  
    - Un **valor cercano a cero** puede deberse a ruido o sistemas neutrales.  
    - Esta métrica se recomienda usar con otras pruebas de no linealidad.
    """)

    if divergencias:
        st.subheader("Visualización de divergencias")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(divergencias, label="log(divergencia relativa)", alpha=0.6)
        ax.set_title("Divergencias entre trayectorias vecinas")
        ax.set_xlabel("Índice")
        ax.set_ylabel("log(|Δxₜ / Δx₀|)")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
