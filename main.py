# main.py

import streamlit as st

# Importar módulos personalizados
from modules.suavizados import mostrar_suavizados
from modules.estadistica import mostrar_estadisticas
from modules.normalidad import mostrar_pruebas_normalidad
from modules.hurst import mostrar_exponente_hurst

st.set_page_config(page_title="Análisis del Precio del Brent", layout="wide")

st.title("Análisis Económico del Precio del Crudo Brent 🛢️")

st.markdown("""
Esta aplicación permite explorar propiedades estadísticas y dinámicas no lineales del Brent, integrando visualizaciones, pruebas estadísticas y herramientas avanzadas como el exponente de Hurst. Ideal para el desarrollo de tesis en econometría, finanzas cuantitativas y econofísica.
""")

opcion = st.sidebar.selectbox(
    "Selecciona un módulo de análisis",
    ("Serie histórica + Suavizados",
     "Estadística Descriptiva",
     "Pruebas de Normalidad",
     "Exponente de Hurst")
)

if opcion == "Serie histórica + Suavizados":
    mostrar_suavizados()
elif opcion == "Estadística Descriptiva":
    mostrar_estadisticas()
elif opcion == "Pruebas de Normalidad":
    mostrar_pruebas_normalidad()
elif opcion == "Exponente de Hurst":
    mostrar_exponente_hurst()
