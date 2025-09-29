# modules/lyapunov.py
import streamlit as st
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import plotly.graph_objects as go

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
    st.header("🔁 Reconstrucción del Espacio de Fases (Atractor tipo Lorenz)")

    st.markdown("""
    Este gráfico tridimensional reconstruye el sistema dinámico del precio del Brent  
    usando **embedding de retardos temporales**.  
    Es similar a los atractores caóticos clásicos (como Lorenz).

    **Explora el gráfico**: puedes rotar, acercar y ver detalles al pasar el cursor.
    """)

    df = cargar_datos()
    serie = df["Brent_Price"].dropna().values

    delay = st.slider("Selecciona el retardo (delay)", 1, 30, 10)

    x, y, z = reconstruccion_espacio_fase(serie, delay)

    fig = go.Figure(data=go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='lines',
        line=dict(color='cyan', width=2),
        opacity=0.8
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title="x(t)",
            yaxis_title=f"x(t + {delay})",
            zaxis_title=f"x(t + {2*delay})",
            bgcolor="black"
        ),
        paper_bgcolor="black",
        font=dict(color="white"),
        title=f"Atractor reconstruido desde serie del Brent (delay={delay})",
        margin=dict(l=0, r=0, b=0, t=40)
    )

    st.plotly_chart(fig, use_container_width=True)
