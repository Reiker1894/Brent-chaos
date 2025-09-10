# modules/estadistica.py
def mostrar_estadisticas():
import streamlit as st
import pandas_datareader.data as web
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


start = "1987-05-20"
end = datetime.today().strftime("%Y-%m-%d")
df = web.DataReader("DCOILBRENTEU", "fred", start, end).dropna()
df = df.rename(columns={"DCOILBRENTEU": "Brent_Price"})


df_diaria = df.copy()
df_semanal = df.resample('W').mean()
df_mensual = df.resample('M').mean()


st.subheader("Estadísticas Descriptivas")


desc_diaria = df_diaria.describe().T.assign(Frecuencia="Diaria")
desc_semanal = df_semanal.describe().T.assign(Frecuencia="Semanal")
desc_mensual = df_mensual.describe().T.assign(Frecuencia="Mensual")


df_stats = pd.concat([desc_diaria, desc_semanal, desc_mensual])
st.dataframe(df_stats, use_container_width=True)


st.subheader("Serie Histórica")
fig, ax = plt.subplots(figsize=(14,7))
ax.plot(df_diaria.index, df_diaria["Brent_Price"], label="Diaria", alpha=0.3)
ax.plot(df_semanal.index, df_semanal["Brent_Price"], label="Semanal", linewidth=1.5)
ax.plot(df_mensual.index, df_mensual["Brent_Price"], label="Mensual", linewidth=2)
ax.set_title("Serie histórica del Brent")
ax.set_xlabel("Fecha")
ax.set_ylabel("USD/barril")
ax.legend()
ax.grid(True)
st.pyplot(fig)
    - Estas características refuerzan la necesidad de modelos no lineales y robustos.
    """)

