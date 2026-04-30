import streamlit as st
import pandas as pd
import json
import os

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="GALA DE LOS 13 PRO", layout="wide")

# 2. AUTENTICACIÓN (BLOQUE DE ENTRADA)
if 'auth' not in st.session_state: 
    st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🏆 Gala de los 13</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Poeta ¿Deseas hacer un Máster con 13 nuevos maestros?</p>", unsafe_allow_html=True)
        
        clave = st.text_input("Introduce la clave para iniciar:", type="password")
        
        if clave == "poeta1208": 
            st.session_state.auth = True
            st.rerun()
        elif clave != "":
            st.error("Clave incorrecta, intenta de nuevo.")
    st.stop() # Solo se detiene si NO está autenticado

# --- TODO LO QUE SIGUE SOLO SE EJECUTA SI LA CLAVE ES CORRECTA ---

# 3. ESTILOS VISUALES
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: white; }
    .mesa-container { 
        display: grid; grid-template-columns: 1fr 1.5fr 1fr; grid-template-rows: 1fr 1.2fr 1fr; 
        gap: 5px; width: 280px; height: 200px; margin: 10px auto; text-align: center; 
    }
    .pos-label { 
        padding: 5px; border-radius: 5px; font-weight: bold; font-size: 13px; color: white; 
        display: flex; align-items: center; justify-content: center; min-height: 40px;
    }
    .pareja1 { background-color: #6b21a8; border: 1px solid #a855f7; } 
    .pareja2 { background-color: #065f46; border: 1px solid #10b981; }
    .mesa-center { 
        grid-column: 2; grid-row: 2; background: #334155; border: 2px dashed #fbbf24; 
        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
        color: #fbbf24; font-weight: bold; font-size: 14px; 
    }
    </style>
""", unsafe_allow_html=True)

# 4. BASE DE DATOS Y PERSISTENCIA
FILE = "memoria_torneo.json"
def cargar_datos():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f: return json.load(f)
        except: pass
    return {"puntos": [], "nombres": {f"j{i}": f"Maestro {i}" for i in range(1, 14)}}

if 'datos' not in st.session_state: 
    st.session_state.datos = cargar_datos()

# 5. LÓGICA DE RONDAS (Mantenemos tu estructura de 13 rondas)
def obtener_ronda(r):
    rondas = {
        1: {"desc": "j13", "m1": ["j1", "j12", "j8", "j5"], "m2": ["j2", "j11", "j3", "j10"], "m3": ["j4", "j9", "j6", "j7"]},
        2: {"desc": "j1", "m1": ["j2", "j13", "j9", "j6"], "m2": ["j3", "j12", "j4", "j11"], "m3": ["j5", "j10", "j7", "j8"]},
        3: {"desc": "j2", "m1": ["j3", "j1", "j10", "j7"], "m2": ["j4", "j13", "j5", "j12"], "m3": ["j6", "j11", "j8", "j9"]},
        4: {"desc": "j3", "m1": ["j4", "j2", "j11", "j8"], "m2": ["j5", "j1", "j6", "j13"], "m3": ["j7", "j12", "j9", "j10"]},
        5: {"desc": "j4", "m1": ["j5", "j3", "j12", "j9"], "m2": ["j6", "j2", "j7", "j1"], "m3": ["j8", "j13", "j10", "j11"]},
        6: {"desc": "j5", "m1": ["j6", "j4", "j13", "j10"], "m2": ["j7", "j3", "j8", "j2"], "m3": ["j9", "j1", "j11", "j12"]},
        7: {"desc": "j6", "m1": ["j7", "j5", "j1", "j11"], "m2": ["j8", "j4", "j9", "j3"], "m3": ["j10", "j2", "j12", "j13"]},
        8: {"desc": "j7", "m1": ["j8", "j6", "j2", "j12"], "m2": ["j9", "j5", "j10", "j4"], "m3": ["j11", "j3", "j13", "j1"]},
        9: {"desc": "j8", "m1": ["j9", "j7", "j3", "j13"], "m2": ["j10", "j6", "j11", "j5"], "m3": ["j12", "j4", "j1", "j2"]},
        10: {"desc": "j9", "m1": ["j10", "j8", "j4", "j1"], "m2": ["j11", "j7", "j12", "j6"], "m3": ["j13", "j5", "j2", "j3"]},
        11: {"desc": "j10", "m1": ["j11", "j9", "j5", "j2"], "m2": ["j12", "j8", "j13", "j7"], "m3": ["j1", "j6", "j3", "j4"]},
        12: {"desc": "j11", "m1": ["j12", "j10", "j6", "j3"], "m2": ["j13", "j9", "j1", "j8"], "m3": ["j2", "j7", "j4", "j5"]},
        13: {"desc": "j12", "m1": ["j13", "j11", "j7", "j4"], "m2": ["j1", "j10", "j2", "j9"], "m3": ["j3", "j8", "j5", "j6"]},
    }
    return rondas.get(r)

# 6. PANEL LATERAL (NOMBRES)
with st.sidebar:
    st.header("⚙️ MAESTROS")
    for i in range(1, 14):
        k = f"j{i}"
        st.session_state.datos["nombres"][k] = st.text_input(f"Jugador {i}", st.session_state.datos["nombres"][k])
    if st.button("💾 Guardar Nombres"):
        with open(FILE, "w") as f: json.dump(st.session_state.datos, f)
        st.success("¡Nombres actualizados!")

# 7. CUERPO PRINCIPAL
r_actual = st.select_slider("SELECCIONAR RONDA", options=list(range(1, 14)))
d, n = obtener_ronda(r_actual), st.session_state.datos["nombres"]

tabs = st.tabs(["📝 CARGA DE RESULTADOS", "🖼️ VISTA DE MESAS", "📊 TABLA DE POSICIONES"])

with tabs[0]:
    st.subheader(f"Ronda {r_actual} - Maestro en Reposo: {n[d['desc']]}")
    def fila_resultado(num, jug):
        st.markdown(f"**MESA {num}**")
        c1, c2 = st.columns(2)
        pa = c1.number_input(f"Puntos {n[jug[0]]} y {n[jug[1]]}", 0, 200, key=f"pa_{r_actual}_{num}")
        pb = c2.number_input(f"Puntos {n[jug[3]]} y {n[jug[2]]}", 0, 200, key=f"pb_{r_actual}_{num}")
        return {"r": r_actual, "j": jug, "pa": pa, "pb": pb}
    
    res = [fila_resultado(1, d["m1"]), fila_resultado(2, d["m2"]), fila_resultado(3, d["m3"])]
    if st.button("🔔 REGISTRAR RONDA"):
        st.session_state.datos["puntos"] = [p for p in st.session_state.datos["puntos"] if p["r"] != r_actual]
        st.session_state.datos["puntos"].extend(res)
        with open(FILE, "w") as f: json.dump(st.session_state.datos, f)
        st.balloons()
        st.success("¡Resultados guardados!")

with tabs[1]:
    def dibujar_mesa(num, jug):
        # ORDEN ANTIHORARIO VALIDADO CON IMAGEN image_6e86be.png
        st.markdown(f'''
            <div class="mesa-container">
                <div class="pos-label pareja1" style="grid-column:2; grid-row:1;">{n[jug[0]]}</div>
                <div class="pos-label pareja2" style="grid-column:3; grid-row:2;">{n[jug[3]]}</div>
                <div class="mesa-center">MESA {num}</div>
                <div class="pos-label pareja1" style="grid-column:2; grid-row:3;">{n[jug[1]]}</div>
                <div class="pos-label pareja2" style="grid-column:1; grid-row:2;">{n[jug[2]]}</div>
            </div>
        ''', unsafe_allow_html=True)
    
    m_cols = st.columns(3)
    for i, m_key in enumerate(["m1", "m2", "m3"]): 
        with m_cols[i]: dibujar_mesa(i+1, d[m_key])

with tabs[2]:
    stats = []
    for k, nom in n.items():
        jg, df = 0, 0
        for p in st.session_state.datos["puntos"]:
            if k in p["j"][:2]: # Pareja morada
                if p["pa"] > p["pb"]: jg += 1
                df += (p["pa"] - p["pb"])
            elif k in p["j"][2:]: # Pareja verde
                if p["pb"] > p["pa"]: jg += 1
                df += (p["pb"] - p["pa"])
        stats.append({'Maestro': nom, 'JG': jg, 'DIF': df})
    
    df_rank = pd.DataFrame(stats).sort_values(['JG', 'DIF'], ascending=False).reset_index(drop=True)
    df_rank.index += 1
    st.table(df_rank)
