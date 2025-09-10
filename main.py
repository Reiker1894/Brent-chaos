import streamlit as st
from modules.suavizados import mostrar_suavizados
from modules.estadisticas import mostrar_estadisticas
from modules.hurst import mostrar_hurst

st.set_page_config(page_title="Análisis del Precio del Brent", layout="wide")

st.sidebar.title("Navegación")
secciones = [
    "Inicio",
    "Suavizados",
    "Estadísticas",
    "Hurst"
]
seleccion = st.sidebar.radio("Ir a:", secciones)

if seleccion == "Inicio":
    st.title("Análisis Multiescala del Precio del Brent")
    st.markdown("""
    Esta aplicación interactiva permite explorar el comportamiento histórico del precio del petróleo Brent usando visualizaciones, estadísticas y técnicas de análisis como el exponente de Hurst. 

    Puedes navegar entre las secciones usando el menú lateral para visualizar:
    - Suavizados de la serie diaria
    - Estadísticas descriptivas y distribuciones
    - Cálculo e interpretación del exponente de Hurst
    """)

elif seleccion == "Suavizados":
    mostrar_suavizados()

elif seleccion == "Estadísticas":
    mostrar_estadisticas()

elif seleccion == "Hurst":
    mostrar_hurst()
