# modules/normalidad.py

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, normaltest, jarque_bera

@st.cache_data
def cargar_datos():
    data = yf.download("BZ=F", start="1990-01-01")
    data = data[['Adj Close']].rename(columns={'Adj Close': 'Brent_Price'})
    data.dropna(inplace=True)
    return data

def mostrar_pruebas_normalidad():
    st.header("Pruebas de Normalidad para el Precio del Brent")
    df = cargar_datos()

    fecha_inicio = st.date_input("Fecha de inicio", df.index.min().date(), key='n_inicio')
    fecha_fin = st.date_input("Fecha de fin", df.index.max().date(), key='n_fin')

    if fecha_inicio >= fecha_fin:
        st.error("La fecha de inicio debe ser anterior a la fecha de fin.")
        return

    df_filtrado = df[(df.index >= pd.to_datetime(fecha_inicio)) & (df.index <= pd.to_datetime(fecha_fin))]

    if df_filtrado.empty:
        st.warning("No hay datos para el rango seleccionado.")
        return

    st.subheader("Pruebas de Normalidad")
    x = df_filtrado['Brent_Price']
    shapiro_test = shapiro(x)
    dagostino_test = normaltest(x)
    jb_test = jarque_bera(x)

    resultados = pd.DataFrame({
        "Prueba": ["Shapiro-Wilk", "D'Agostino-Pearson", "Jarque-Bera"],
        "Estadístico": [shapiro_test.statistic, dagostino_test.statistic, jb_test.statistic],
        "p-valor": [shapiro_test.pvalue, dagostino_test.pvalue, jb_test.pvalue],
        "Conclusión": [
            "Rechaza normalidad" if shapiro_test.pvalue < 0.05 else "No se rechaza",
            "Rechaza normalidad" if dagostino_test.pvalue < 0.05 else "No se rechaza",
            "Rechaza normalidad" if jb_test.pvalue < 0.05 else "No se rechaza"
        ]
    })

    st.dataframe(resultados, use_container_width=True)

    st.subheader("QQ Plot")
    from statsmodels.graphics.gofplots import qqplot
    fig, ax = plt.subplots(figsize=(6,6))
    qqplot(x, line='s', ax=ax)
    ax.set_title("Gráfico Q-Q para evaluar normalidad")
    st.pyplot(fig)

    st.markdown("""
    **Interpretación sugerida:**
    - Si los p-valores son menores a 0.05, se rechaza la normalidad (alta probabilidad de distribuciones no normales).
    - El QQ-Plot revela visualmente desviaciones de la normalidad""")
