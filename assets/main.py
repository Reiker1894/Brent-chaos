
# main.py
import streamlit as st

st.set_page_config(layout="wide", page_title="Tesis - Análisis Brent & Caos")

st.sidebar.title("Menú")
opcion = st.sidebar.selectbox("Selecciona análisis", [
    "Inicio",
    "Serie histórica + Suavizados",
    "Estadística descriptiva",
    "Normalidad",
    "Hurst exponent",
    "Multiescala"
])

if opcion == "Inicio":
    st.title("Análisis de Caos y Fractalidad en el Brent")
    st.markdown("""
    Bienvenido al panel interactivo de avances de tesis.
    
    Aquí se muestran los análisis estadísticos, fractales y de caos aplicados al precio del crudo Brent.
    
    **Fecha actual**: Septiembre 2025  
    **Objetivo**: Explorar evidencia de dinámica compleja (no lineal, caótica, autosimilar) en el mercado energético.
    """)
    
elif opcion == "Serie histórica + Suavizados":
    from modules.suavizados import mostrar_suavizados
    mostrar_suavizados()

elif opcion == "Estadística descriptiva":
    from modules.estadistica import mostrar_estadisticas
    mostrar_estadisticas()

elif opcion == "Normalidad":
    from modules.normalidad import test_normalidad
    test_normalidad()

elif opcion == "Hurst exponent":
    from modules.hurst import calcular_hurst
    calcular_hurst()

elif opcion == "Multiescala":
    from modules.multiscale import grafico_multiescala
    grafico_multiescala()
