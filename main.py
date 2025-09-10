# Estructura de tu proyecto en GitHub

# brent-chaos/
# ├── app.py                ← App principal Streamlit
# ├── requirements.txt     ← Dependencias
# ├── data_utils.py         ← Descarga y limpieza
# ├── analysis.py           ← Estadísticas, normalidad, Hurst, etc.
# └── plots.py              ← Gráficos

import streamlit as st
from modules.estadistica import mostrar_estadisticas
from modules.normalidad import mostrar_pruebas_normalidad
from modules.hurst import mostrar_exponente_hurst
from modules.suavizados import mostrar_suavizados


st.set_page_config(layout="wide", page_title="Análisis del Brent")


st.title("Dashboard de Análisis del Precio del Brent")


opciones = ["Estadísticas Generales", "Suavizados", "Pruebas de Normalidad", "Exponente de Hurst"]
opcion = st.sidebar.radio("Selecciona un análisis:", opciones)


if opcion == "Estadísticas Generales":
mostrar_estadisticas()
elif opcion == "Suavizados":
mostrar_suavizados()
elif opcion == "Pruebas de Normalidad":
mostrar_pruebas_normalidad()
elif opcion == "Exponente de Hurst":
mostrar_exponente_hurst()
