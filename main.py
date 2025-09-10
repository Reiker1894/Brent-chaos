import streamlit as st
from modules.suavizados import mostrar_suavizados
from modules.estadistica import mostrar_estadisticas
from modules.hurst import mostrar_hurst
import streamlit.components.v1 as components

st.set_page_config(page_title="Maestría en Ciencias Económicas", layout="wide")
# --- Fondo personalizado (si tienes background.html) ---
# components.html(open("background.html", "r").read(), height=0, width=0)
# # --- Configuración de página ---


st.sidebar.title("Navegación")
secciones = [
    "Inicio",
    "Suavizados",
    "Estadísticas",
    "Hurst"
]
seleccion = st.sidebar.radio("Ir a:", secciones)

if seleccion == "Inicio":
    st.title("Pronósticos del precio del Brent utilizando medidas de caos y modelos de Machine Learnin")
    st.markdown("""
   El pronóstico del precio del Brent se sustenta en la literatura sobre mercados financieros complejos, caos y aprendizaje automático. Tradicionalmente, la formación de precios en los activos financieros se explicaba bajo la Hipótesis de Mercados Eficientes, que asume racionalidad, información perfecta y series temporales independientes e idénticamente distribuidas (I.I.D). Sin embargo, la evidencia empírica muestra que los precios presentan comportamientos no lineales, colas pesadas, y memoria de largo plazo, lo que sugiere que los mercados no están en equilibrio constante.

Se propone entonces abordar esta complejidad mediante herramientas de la econofísica, incluyendo:

Exponente de Hurst: Indica la presencia de persistencia o anti-persistencia en las series.

Dimensión fractal y Exponentes de Lyapunov: Revelan la estructura caótica y la predictibilidad de los precios.

Entropías (Shannon, Rényi, SVD, etc.): Miden la incertidumbre y complejidad de las series.

Este enfoque permite combinar estas medidas de complejidad con modelos de Machine Learning como KNN, Random Forest, XGBoost, SVM, ANN y LSTM, lo cual mejora significativamente los pronósticos al capturar la naturaleza no lineal y dinámica del mercado del crudo.

El objetivo general es doble:

1. Identificar escalas temporales donde existe autosimilitud o procesos persistentes.

2. Usar estas señales para entrenar modelos predictivos más robustos y precisos.

Referencias clave incluyen trabajos de Mandelbrot (1963), Peters (1999), Moshiri y Foroutan (2006), y Raubitzek y Thomas (2021).
    """)

elif seleccion == "Suavizados":
    mostrar_suavizados()

elif seleccion == "Estadísticas":
    mostrar_estadisticas()

elif seleccion == "Hurst":
    mostrar_hurst()
