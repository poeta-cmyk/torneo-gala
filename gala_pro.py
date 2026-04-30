import streamlit as st  # <--- ESTO DEBE IR PRIMERO
import pandas as pd
import json
import os

# 1. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="GALA DE LOS 13 PRO", layout="wide")

# 2. AUTENTICACIÓN CON SALUDO PERSONALIZADO
if 'auth' not in st.session_state: 
    st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🏆 Gala de los 13</h2>", unsafe_allow_html=True)
        # El saludo para el Maestro Franz Lameda
        st.markdown("<p style='text-align: center; font-size: 18px; font-weight: bold;'>Poeta ¿Deseas hacer un Máster con 13 nuevos maestros?</p>", unsafe_allow_html=True)
        
        clave = st.text_input("Introduce la clave para iniciar:", type="password")
        
        if clave == "poeta1208": 
            st.session_state.auth = True
            st.rerun()
        elif clave != "":
            st.error("Clave incorrecta, intenta de nuevo.")
    st.stop()

# EL RESTO DEL CÓDIGO (ESTILOS, BASE DE DATOS, ETC.) SIGUE ABAJO...
