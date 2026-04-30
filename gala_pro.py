import streamlit as st
import pandas as pd
import json
import os
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="GALA DE LOS 13 PRO", layout="wide")

# --- 2. BASE DE DATOS ---
FILE = "memoria_torneo.json"

def cargar_db():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except: pass
    return {"puntos": [], "nombres": {f"j{i}": f"Maestro {i}" for i in range(1, 14)}}

if 'db' not in st.session_state:
    st.session_state.db = cargar_db()

# --- 3. FLUJO DE ENTRADA ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'decidido' not in st.session_state: st.session_state.decidido = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><h2 style='text-align: center;'>🏆 Gala de los 13</h2>", unsafe_allow_html=True)
        clave = st.text_input("Introduce la clave:", type="password", key="p_acceso")
        if clave == "poeta1208":
            st.session_state.auth = True
            st.rerun()
    st.stop()

if not st.session_state.decidido:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><h3 style='text-align: center; color: #fbbf24;'>Poeta ¿Deseas hacer un Máster con 13 nuevos maestros?</h3>", unsafe_allow_html=True)
        c_si, c_no = st.columns(2)
        if c_si.button("✅ SÍ (Borrar todo)", use_container_width=True):
            st.session_state.db = {"puntos": [], "nombres": {f"j{i}": f"Maestro {i}" for i in range(1, 14)}}
            with open(FILE, "w") as f: json.dump(st.session_state.db, f)
            st.session_state.decidido = True
            st.rerun()
        if c_no.button("❌ NO (Mantener datos)", use_container_width=True):
            st.session_state.decidido = True
            st.rerun()
    st.stop()

# --- 4. TEMPORIZADOR DE 35 MINUTOS ---
with st.sidebar:
    st.markdown("### ⏳ Cronómetro de Ronda")
    if 'end_time' not in st.session_state:
        st.session_state.end_time = None

    col_t1, col_t2 = st.columns(2)
    if col_t1.button("▶️ Iniciar 35m"):
        st.session_state.end_time = time.time() + 35 * 60
    if col_t2.button("⏱️ Reset"):
        st.session_state.end_time = None

    placeholder = st.empty()

    if st.session_state.end_time:
        rem = st.session_state.end_time - time.time()
        if rem > 0:
            mins, secs = divmod(int(rem), 60)
            color = "#ef4444" if mins < 5 else "#fbbf24"
            placeholder.markdown(f"<h2 style='text-align: center; color: {color};'>{mins:02d}:{secs:02d}</h2>", unsafe_allow_html=True)
            # Nota: Streamlit no se refresca solo cada segundo sin un loop complejo, 
            # pero al interactuar con la app el tiempo se actualizará.
        else:
            placeholder.markdown("<h2 style='text-align: center; color: #ef4444;'>¡TIEMPO!</h2>", unsafe_allow_html=True)
    else:
        placeholder.markdown("<h2 style='text-align: center; color: gray;'>35:00</h2>", unsafe_allow_html=True)
    
    st.divider()
    st.header("⚙️ Maestros")
    for i in range(1, 14):
        k = f"j{i}"
        st.session_state.db["nombres"][k] = st.text_input(f"ID {i}", st.session_state.db["nombres"][k], key=f"side_{k}")
    if st.button("💾 Guardar"):
        with open(FILE, "w") as f: json.dump(st.session_state.db, f)

# --- 5. TABS PRINCIPALES (CARGA, MESAS, RANKING) ---
# ... (El resto del código de Rondas y Ranking se mantiene igual que el anterior)
r_sel = st.select_slider("RONDA ACTUAL", options=list(range(1, 14)))

# Lógica simplificada para mostrar que el resto sigue igual
st.write(f"Gestionando la Ronda {r_sel}")
# (Aquí irían los mismos Tabs t1, t2, t3 definidos anteriormente)
