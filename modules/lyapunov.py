# modules/lyapunov.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from mpl_toolkits.mplot3d import Axes3D

@st.cache_data
def cargar_datos():
    start = "1987-05-20"
    end = "2025-09-07"
    df = web.DataReader("DCOILBRENTEU", "fred", start, end).dropna()
    df = df.rename(columns={"DCOILBRENTEU": "Brent_Price"})
    return df

def reconstruccion_espacio_fase(data, delay=5):
    x = data[:-2 * delay]
    y = data[delay:-delay]
    z = data[2 * delay:]
    return x, y, z

def mostrar_lyapunov():
    st.header("Reconstrucción en el espacio de fases (Atractor tipo Lorenz)")

    st.markdown("""
    Para visualizar el comportamiento dinámico no lineal de la serie del Brent,  
    reconstruimos su **espacio de fases** con un **embedding 3D** utilizando retardos temporales.
    
    Esta técnica permite identificar patrones **caóticos** similares a los atractores de Lorenz.
    """)

    df = cargar_datos()
    serie = df["Brent_Price"].dropna().values

    delay = st.slider("Selecciona el retardo (delay)", 1, 30, 10)

    x, y, z = reconstruccion_espacio_fase(serie, delay)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, lw=0.5, alpha=0.8)
    ax.set_title(f"Espacio de fases embebido (delay = {delay})")
    ax.set_xlabel("x(t)")
    ax.set_ylabel(f"x(t + {delay})")
    ax.set_zlabel(f"x(t + {2*delay})")
    st.pyplot(fig)

    st.markdown("""
    - Este gráfico tridimensional revela la **estructura interna** del sistema dinámico.  
    - Si el sistema tiene comportamiento **caótico determinista**, debería formarse una estructura similar a un atractor.
    - El retardo óptimo puede ajustarse para obtener mejor separación entre trayectorias.
    """)
