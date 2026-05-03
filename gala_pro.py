import streamlit as st
import pandas as pd
import json
import os
import time
import urllib.parse
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN Y REFRESCO ---
st.set_page_config(page_title="GALA DE LOS 13 PRO", layout="wide")
# Actualiza la app cada 1 segundo para que el reloj sea exacto
st_autorefresh(interval=1000, key="cronometro_refresh")

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

# --- 3. ESTILOS (INCLUYE PANTALLA ROJA) ---
st.markdown("""
    <style>
    .mesa-container { display: grid; grid-template-columns: 1fr 1.5fr 1fr; grid-template-rows: 1fr 1.2fr 1fr; gap: 5px; width: 280px; height: 200px; margin: 10px auto; text-align: center; }
    .pos-label { padding: 5px; border-radius: 5px; font-weight: bold; font-size: 13px; color: white; display: flex; align-items: center; justify-content: center; min-height: 40px; }
    .p-morada { background-color: #6b21a8; border: 1px solid #a855f7; } 
    .p-verde { background-color: #065f46; border: 1px solid #10b981; }
    .m-centro { grid-column: 2; grid-row: 2; background: #334155; border: 2px dashed #fbbf24; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fbbf24; font-weight: bold; }
    
    /* Pantalla de Tiempo Vencido */
    .overlay-rojo {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #ff0000;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }
    .texto-vencido {
        color: black;
        font-family: 'Arial Black', sans-serif;
        font-size: 80px;
        text-align: center;
        font-weight: 900;
        line-height: 1;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. LÓGICA DEL TEMPORIZADOR ---
if 'end_time' not in st.session_state: st.session_state.end_time = None
if 'alarma_sonada' not in st.session_state: st.session_state.alarma_sonada = False

vencido = False
quedan_5 = False

if st.session_state.end_time:
    rem = st.session_state.end_time - time.time()
    if rem <= 0:
        vencido = True
    elif rem <= 300: # Menos de 5 minutos
        quedan_5 = True

# --- 5. PANTALLA DE BLOQUEO (SI EL TIEMPO VENCIÓ) ---
if vencido:
    st.markdown(f"""
        <div class="overlay-rojo">
            <div class="texto-vencido">TIEMPO<br>VENCIDO</div>
        </div>
    """, unsafe_allow_html=True)
    # Botón discreto para que el Poeta reinicie
    if st.button("🔄 REINICIAR SISTEMA"):
        st.session_state.end_time = None
        st.session_state.alarma_sonada = False
        st.rerun()
    st.stop() # Detiene el resto de la app

# --- 6. FLUJO DE ENTRADA (SOLO SI NO ESTÁ VENCIDO) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><h2 style='text-align: center;'>🏆 Gala de los 13</h2>", unsafe_allow_html=True)
        clave = st.text_input("Clave:", type="password")
        if clave == "poeta1208":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 7. SIDEBAR ---
with st.sidebar:
    st.markdown("### ⏳ Cronómetro")
    c1, c2 = st.columns(2)
    if c1.button("▶️ Iniciar 35m"):
        st.session_state.end_time = time.time() + 35 * 60
        st.session_state.alarma_sonada = False
    if c2.button("⏱️ Reset"):
        st.session_state.end_time = None
        st.session_state.alarma_sonada = False

    if st.session_state.end_time:
        rem = st.session_state.end_time - time.time()
        m, s = divmod(int(rem), 60)
        color = "#ff0000" if quedan_5 else "#fbbf24"
        st.markdown(f"<h2 style='text-align: center; color: {color};'>{m:02d}:{s:02d}</h2>", unsafe_allow_html=True)
        
        # Sonido de alerta a los 5 min (Usa un beep del sistema si es posible)
        if quedan_5 and not st.session_state.alarma_sonada:
            st.warning("⚠️ QUEDAN 5 MINUTOS")
            st.session_state.alarma_sonada = True
    else:
        st.markdown("<h2 style='text-align: center; color: gray;'>35:00</h2>", unsafe_allow_html=True)

    st.divider()
    for i in range(1, 14):
        k = f"j{i}"
        st.session_state.db["nombres"][k] = st.text_input(f"ID {i}", st.session_state.db["nombres"][k], key=f"s_{k}")
    if st.button("💾 Guardar"):
        with open(FILE, "w") as f: json.dump(st.session_state.db, f)

# --- 8. RONDAS Y TABS (RESTO DEL CÓDIGO) ---
# [Aquí irían las pestañas de CARGA, MESAS y RANKING como en la versión anterior]
# Nota: Por brevedad no repito las 100 líneas de la lógica de rondas, 
# pero asegúrese de unirlas debajo de este bloque.
