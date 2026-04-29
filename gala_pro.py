import streamlit as st
import pandas as pd
import json
import os

# 1. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="GALA DE LOS 13 PRO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0f172a; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1e293b; border-radius: 8px; padding: 8px 16px; color: #94a3b8;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #38bdf8 !important; color: white !important; 
    }
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

# 2. AUTENTICACIÓN
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🏆 Gala de los 13")
        clave = st.text_input("Clave de Acceso", type="password")
        if clave == "poeta1208": 
            st.session_state.auth = True
            st.rerun()
    st.stop()

# 3. BASE DE DATOS
FILE = "memoria_torneo.json"
def cargar():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f: return json.load(f)
        except: pass
    return {"puntos": [], "nombres": {f"j{i}": f"Maestro {i}" for i in range(1, 14)}}

if 'datos' not in st.session_state: st.session_state.datos = cargar()

# 4. LÓGICA DE RONDAS
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

# 5. SIDEBAR: NOMBRES
with st.sidebar:
    st.header("⚙️ CONFIGURACIÓN")
    for i in range(1, 14):
        k = f"j{i}"
        st.session_state.datos["nombres"][k] = st.text_input(f"Jugador {i}", st.session_state.datos["nombres"][k])
    if st.button("💾 Guardar Nombres"):
        with open(FILE, "w") as f: json.dump(st.session_state.datos, f)
        st.success("Guardado")

# 6. INTERFAZ PRINCIPAL
r_actual = st.select_slider("RONDA", options=list(range(1, 14)))
d, n = obtener_ronda(r_actual), st.session_state.datos["nombres"]

tabs = st.tabs(["📝 CARGA", "🖼️ MESAS", "📊 POSICIONES"])

with tabs[0]:
    st.write(f"🧘 Reposo: **{n[d['desc']]}**")
    def fila(num, jug):
        st.markdown(f"**MESA {num}**")
        c1, c2 = st.columns(2)
        pa = c1.number_input(f"{n[jug[0]]} / {n[jug[1]]}", 0, 200, key=f"pa_{r_actual}_{num}")
        pb = c2.number_input(f"{n[jug[2]]} / {n[jug[3]]}", 0, 200, key=f"pb_{r_actual}_{num}")
        return {"r": r_actual, "j": jug, "pa": pa, "pb": pb}
    
    res = [fila(1, d["m1"]), fila(2, d["m2"]), fila(3, d["m3"])]
    if st.button("🔔 REGISTRAR RESULTADOS"):
        st.session_state.datos["puntos"] = [p for p in st.session_state.datos["puntos"] if p["r"] != r_actual]
        st.session_state.datos["puntos"].extend(res)
        with open(FILE, "w") as f: json.dump(st.session_state.datos, f)
        st.balloons()

with tabs[1]:
    def mesa(num, jug):
        # INVERSIÓN DE FRANJAS VERDES PARA SENTIDO ANTIHORARIO:
        # Arriba (Morado): jug[0]
        # Derecha (Verde): jug[3] (Antes era jug[2])
        # Abajo (Morado): jug[1]
        # Izquierda (Verde): jug[2] (Antes era jug[3])
        st.markdown(f'''
            <div class="mesa-container">
                <div class="pos-label pareja1" style="grid-column:2; grid-row:1;">{n[jug[0]]}</div>
                <div class="pos-label pareja2" style="grid-column:3; grid-row:2;">{n[jug[3]]}</div>
                <div class="mesa-center">MESA {num}</div>
                <div class="pos-label pareja1" style="grid-column:2; grid-row:3;">{n[jug[1]]}</div>
                <div class="pos-label pareja2" style="grid-column:1; grid-row:2;">{n[jug[2]]}</div>
            </div>
        ''', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, m in enumerate(["m1", "m2", "m3"]): 
        with cols[i]: mesa(i+1, d[m])

with tabs[2]:
    stats = []
    for k, nom in n.items():
        jg, df = 0, 0
        for p in st.session_state.datos["puntos"]:
            if k in p["j"][:2]:
                if p["pa"] > p["pb"]: jg += 1
                df += (p["pa"] - p["pb"])
            elif k in p["j"][2:]:
                if p["pb"] > p["pa"]: jg += 1
                df += (p["pb"] - p["pa"])
        stats.append({'Maestro': nom, 'JG': jg, 'DIF': df})
    
    rank = pd.DataFrame(stats).sort_values(['JG', 'DIF'], ascending=False).reset_index(drop=True)
    rank.index += 1
    st.table(rank)
