import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, shapiro, normaltest, jarque_bera


@st.cache_data
def cargar_datos():
df = pd.read_csv("https://raw.githubusercontent.com/datasets/brent-crude/master/data/brent-daily.csv")
df.columns = ["Date", "Brent_Price"]
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)
return df


def calcular_estadisticas_normalidad(df, label):
x = df["Brent_Price"].dropna()
return {
"Frecuencia": label,
"Media": x.mean(),
"Desv.Std": x.std(),
"Asimetría": skew(x),
"Curtosis": kurtosis(x),
"Shapiro-Wilk p": shapiro(x.sample(500) if len(x) > 500 else x)[1],
"Jarque-Bera p": jarque_bera(x)[1],
"D’Agostino p": normaltest(x)[1]
}


def mostrar_pruebas_normalidad():
st.header("Pruebas de Normalidad para el Precio del Brent")
df = cargar_datos()


df_diaria = df.copy()
df_semanal = df.resample('W').mean()
df_mensual = df.resample('M').mean()


resultados = pd.DataFrame([
calcular_estadisticas_normalidad(df_diaria, "Diaria"),
calcular_estadisticas_normalidad(df_semanal, "Semanal"),
calcular_estadisticas_normalidad(df_mensual, "Mensual")
])


st.subheader("Resultados de pruebas de normalidad")
st.dataframe(resultados, use_container_width=True)


# Histograma + KDE
st.subheader("Distribuciones con KDE")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, data, label, color in zip(
axes,
[df_diaria, df_semanal, df_mensual],
["Diaria", "Semanal", "Mensual"],
["blue", "green", "orange"]):
sns.histplot(data["Brent_Price"], bins=30, kde=True, color=color, stat="density", edgecolor="black", ax=ax)
ax.set_title(f"Histograma + KDE - {label}")
ax.set_xlabel("Precio Brent (USD)")
st.pyplot(fig)


st.markdown("""
**Interpretación sugerida:**
- Si los p-valores son menores a 0.05, se rechaza la hipótesis de normalidad.
- Asimetría y curtosis muestran la forma de la distribución.
- El histograma y KDE ayudan a visualizar la desviación de la normalidad.
""")
