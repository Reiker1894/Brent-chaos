# modules/lyapunov.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nolds  # <-- librería especializada

@st.cache_data
def cargar_datos():
    start = "1987-05-20"
    end = "2025-09-07"
    df = pd.read_csv("data/brent_diario.csv", parse_dates=["Date"])
    df.set_index("Date", inplace=True)
    return df

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
    serie = df["Brent_Price"].dropna().values[-3000:]  # Recorta si es muy grande

    # Parámetros de embedding
    emb_dim = st.slider("Dimensión del Embedding (m)", 2, 15, 6)
    tau = st.slider("Retraso temporal (tau)", 1, 20, 2)

    try:
        lyap = nolds.lyap_r(serie, emb_dim=emb_dim, lag=tau, debug_plot=True)
        st.subheader("Resultado del Exponente")
        st.metric("Lyapunov estimado", f"{lyap:.6f}")

        st.markdown("""
        - Un **valor positivo** indica evidencia potencial de caos determinista.  
        - Un **valor cercano a cero** puede deberse a ruido o sistemas neutrales.  
        - Esta métrica se recomienda usar con otras pruebas de no linealidad.
        """)
        
    except Exception as e:
        st.error(f"Error al calcular Lyapunov: {e}")
