import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader.data as web

@st.cache_data
def cargar_datos():
    start = "1987-05-20"
    end = "2025-09-07"
    df = web.DataReader("DCOILBRENTEU", "fred", start, end).dropna()
    df = df.rename(columns={"DCOILBRENTEU": "Brent_Price"})
    return df

def mostrar_estadisticas():
    st.header("Estadísticas Descriptivas del Precio del Brent")

    df = cargar_datos()

    # Crear versiones re-muestreadas
    df_diaria = df.copy()
    df_semanal = df.resample('W').mean()
    df_mensual = df.resample('M').mean()

    # Estadísticas
    desc_diaria = df_diaria.describe().T.assign(Frecuencia="Diaria")
    desc_semanal = df_semanal.describe().T.assign(Frecuencia="Semanal")
    desc_mensual = df_mensual.describe().T.assign(Frecuencia="Mensual")

    df_stats = pd.concat([desc_diaria, desc_semanal, desc_mensual])

    st.dataframe(df_stats, use_container_width=True)

    # Histogramas
    st.subheader("Distribución de Precios con KDE")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, data, label, color in zip(axes,
                                      [df_diaria, df_semanal, df_mensual],
                                      ["Diaria", "Semanal", "Mensual"],
                                      ["blue", "green", "orange"]):
        sns.histplot(data["Brent_Price"], bins=30, kde=True, color=color, stat="density", edgecolor="black", ax=ax)
        ax.set_title(f"Histograma + KDE - Frecuencia {label}")
        ax.set_xlabel("Precio Brent (USD)")
        ax.set_ylabel("Densidad")
        ax.grid(True)

    st.pyplot(fig)
