# modules/lyapunov.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nolds
import pandas_datareader.data as web

@st.cache_data
def cargar_datos():
    start = "1987-05-20"
    end = "2025-09-07"
    df = web.DataReader("DCOILBRENTEU", "fred", start, end).dropna()
    df = df.rename(columns={"DCOILBRENTEU": "Brent_Price"})
    return df

def mostrar_lyapunov():
    st.header("Exponente de Lyapunov (nolds)")

    st.markdown("""
    El **exponente de Lyapunov** mide la sensibilidad a las condiciones iniciales.  
    Este valor ayuda a determinar si una serie temporal muestra **comportamiento caótico**:
    
    - **H > 0**: Caos determinista (sensible a condiciones iniciales).
    - **H ≈ 0**: Comportamiento aleatorio o neutro.
    - **H < 0**: Sistema estable (sin divergencia de trayectorias).

    Esta estimación se realiza con `nolds.lyap_r`, un método robusto basado en retrasos temporales.
    """)

    df = cargar_datos()
    serie = df["Brent_Price"].dropna().values

    lyap_exp = nolds.lyap_r(serie, emb_dim=10, lag=1, min_tsep=10,  debug_plot=True)

    st.subheader("Resultado del Exponente de Lyapunov")
    st.metric("Lyapunov estimado", f"{lyap_exp:.6f}")

    st.markdown("""
    - Un valor **positivo y significativo** indica posible evidencia de **caos determinista**.
    - Este análisis es útil para estudiar series temporales financieras con dinámica no lineal.
    """)
    except Exception as e:
        st.error(f"Error al calcular Lyapunov: {e}")
