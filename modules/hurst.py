import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader.data as web
import numpy as np
from scipy.stats import skew, kurtosis, shapiro, normaltest, jarque_bera

@st.cache_data
def cargar_datos():
    start = "1987-05-20"
    end = "2025-09-07"
    df = web.DataReader("DCOILBRENTEU", "fred", start, end).dropna()
    df = df.rename(columns={"DCOILBRENTEU": "Brent_Price"})
    return df

def hurst_exponent(ts, max_lag=100):
    lags = range(2, max_lag)
    tau = []
    for lag in lags:
        chunks = [ts[i:i+lag] for i in range(0, len(ts) - lag, lag)]
        rs_values = []
        for chunk in chunks:
            if len(chunk) < lag:
                continue
            Y = chunk - np.mean(chunk)
            Z = np.cumsum(Y)
            R = max(Z) - min(Z)
            S = np.std(chunk)
            if S != 0:
                rs_values.append(R / S)
        if len(rs_values) > 0:
            tau.append(np.mean(rs_values))
        else:
            tau.append(np.nan)
    log_lags = np.log10(list(lags))
    log_tau = np.log10(tau)
    mask = ~np.isnan(log_tau)
    hurst, _ = np.polyfit(log_lags[mask], log_tau[mask], 1)
    return hurst

def plot_hurst_rs(ts, max_lag=100, title=''):
    lags = range(2, max_lag)
    tau = []
    for lag in lags:
        chunks = [ts[i:i+lag] for i in range(0, len(ts) - lag, lag)]
        rs_values = []
        for chunk in chunks:
            if len(chunk) < lag:
                continue
            Y = chunk - np.mean(chunk)
            Z = np.cumsum(Y)
            R = max(Z) - min(Z)
            S = np.std(chunk)
            if S != 0:
                rs_values.append(R / S)
        if len(rs_values) > 0:
            tau.append(np.mean(rs_values))
        else:
            tau.append(np.nan)
    log_lags = np.log10(list(lags))
    log_tau = np.log10(tau)
    mask = ~np.isnan(log_tau)
    slope, intercept = np.polyfit(log_lags[mask], log_tau[mask], 1)
    plt.figure(figsize=(8,6))
    plt.plot(log_lags, log_tau, 'o', label="log(R/S)")
    plt.plot(log_lags, slope * log_lags + intercept, 'r--', label=f'Ajuste lineal (H = {slope:.4f})')
    plt.title(f'Gráfico log(R/S) vs log(n) - {title}')
    plt.xlabel("log(n)")
    plt.ylabel("log(R/S)")
    plt.grid(True)
    plt.legend()
    st.pyplot(plt.gcf())

def mostrar_exponente_hurst():
    st.header("Exponente de Hurst")

    df = cargar_datos()
    df_diaria = df.copy()
    df_semanal = df.resample('W').mean()
    df_mensual = df.resample('M').mean()

    H_diaria = hurst_exponent(df_diaria['Brent_Price'])
    H_semanal = hurst_exponent(df_semanal['Brent_Price'])
    H_mensual = hurst_exponent(df_mensual['Brent_Price'])

    st.write("**Exponentes de Hurst:**")
    st.write(f"- Diaria: {H_diaria:.4f}")
    st.write(f"- Semanal: {H_semanal:.4f}")
    st.write(f"- Mensual: {H_mensual:.4f}")

    st.subheader("Visualización log-log del análisis R/S")
    frecuencia = st.selectbox("Selecciona la frecuencia para visualizar", ["Diaria", "Semanal", "Mensual"])

    if frecuencia == "Diaria":
        plot_hurst_rs(df_diaria['Brent_Price'].values, title='Brent - Frecuencia Diaria')
    elif frecuencia == "Semanal":
        plot_hurst_rs(df_semanal['Brent_Price'].values, title='Brent - Frecuencia Semanal')
    else:
        plot_hurst_rs(df_mensual['Brent_Price'].values, title='Brent - Frecuencia Mensual')
