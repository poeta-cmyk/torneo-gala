import streamlit as st
import pandas as pd
import json
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="GALA DE LOS 13 PRO", layout="wide")

# --- 2. CONTROL DE ACCESO (AUTENTICACIÓN) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><h2 style='text-align: center;'>🏆 Gala de los 13</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Poeta ¿Deseas hacer un Máster con 13 nuevos maestros?</p>", unsafe_allow_html=True)
        
        clave = st.text_input("Introduce la clave:", type="password", key="login_key")
        if clave == "poeta1208":
            st.session_state.auth = True
            st.rerun()
        elif clave != "":
            st.error("Clave incorrecta")
    st.stop()

# --- 3. ESTILOS CSS ---
st.markdown("""
    <style>
    .mesa-container { 
        display: grid; grid-template-columns: 1fr 1.5fr 1fr; grid-template-rows: 1fr 1.2fr 1fr; 
        gap: 5px; width: 280px; height: 200px; margin: 10px auto; text-align: center; 
    }
    .pos-label { 
        padding: 5px; border-radius: 5px; font-weight: bold; font-size: 13px; color: white; 
        display: flex; align-items: center; justify-content: center; min-height: 40px;
    }
    .pareja-morada { background-color: #6b21a8; border: 1px solid #a855f7; } 
    .pareja-verde { background-color: #065f46; border: 1px solid #10b981; }
    .mesa-centro { 
        grid-column: 2; grid-row: 2; background: #334155; border: 2px dashed #fbbf24; 
        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
        color: #fbbf24; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. PERSISTENCIA DE DATOS ---
FILE = "torneo_data.json"
def cargar_db():
    if os.path.exists(FILE):
        with open(FILE, "r") as f: return json.load(f)
    return {"puntos": [], "nombres": {f"j{i}": f"Maestro {i}" for i in range(1, 14)}}

if 'db' not in st.session_state:
    st.session_state.db = cargar_db()

# --- 5. DEFINICIÓN DE RONDAS ---
def get_ronda(r):
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

# --- 6. SIDEBAR: NOMBRES ---
with st.sidebar:
    st.header("Maestros")
    for i in range(1, 14):
        id_j = f"j{i}"
        st.session_state.db["nombres"][id_j] = st.text_input(f"ID {i}", st.session_state.db["nombres"][id_j], key=f"input_{id_j}")
    if st.button("Guardar Nombres"):
        with open(FILE, "w") as f: json.dump(st.session_state.db, f)
        st.success("Nombres Guardados")

# --- 7. CONTENIDO PRINCIPAL ---
r_sel = st.select_slider("Ronda del Torneo", options=list(range(1, 14)))
r_data, nombres = get_ronda(r_sel), st.session_state.db["nombres"]

t1, t2, t3 = st.tabs(["Carga", "Mesas", "Ranking"])

with t1:
    st.write(f"Libre: {nombres[r_data['desc']]}")
    def capturar(n_mesa, ids):
        st.subheader(f"Mesa {n_mesa}")
        c1, c2 = st.columns(2)
        p1 = c1.number_input(f"{nombres[ids[0]]} / {nombres[ids[1]]}", 0, 200, key=f"r{r_sel}m{n_mesa}p1")
        p2 = c2.number_input(f"{nombres[ids[2]]} / {nombres[ids[3]]}", 0, 200, key=f"r{r_sel}m{n_mesa}p2")
        return {"r": r_sel, "j": ids, "pa": p1, "pb": p2}
    
    actuales = [capturar(1, r_data["m1"]), capturar(2, r_data["m2"]), capturar(3, r_data["m3"])]
    if st.button("Registrar Resultados"):
        st.session_state.db["puntos"] = [p for p in st.session_state.db["puntos"] if p["r"] != r_sel]
        st.session_state.db["puntos"].extend(actuales)
        with open(FILE, "w") as f: json.dump(st.session_state.db, f)
        st.balloons()

with t2:
    def mostrar_mesa(n_mesa, ids):
        # ORDEN ANTIHORARIO ESTRICTO (image_6e86be.png)
        st.markdown(f'''
            <div class="mesa-container">
                <div class="pos-label pareja-morada" style="grid-column:2; grid-row:1;">{nombres[ids[0]]}</div>
                <div class="pos-label pareja-verde" style="grid-column:3; grid-row:2;">{nombres[ids[3]]}</div>
                <div class="mesa-centro">M {n_mesa}</div>
                <div class="pos-label pareja-morada" style="grid-column:2; grid-row:3;">{nombres[ids[1]]}</div>
                <div class="pos-label pareja-verde" style="grid-column:1; grid-row:2;">{nombres[ids[2]]}</div>
            </div>
        ''', unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1: mostrar_mesa(1, r_data["m1"])
    with col_m2: mostrar_mesa(2, r_data["m2"])
    with col_m3: mostrar_mesa(3, r_data["m3"])

with t3:
    final = []
    for k, nom in nombres.items():
        jg, dif = 0, 0
        for p in st.session_state.db["puntos"]:
            if k in p["j"][:2]:
                if p["pa"] > p["pb"]: jg += 1
                dif += (p["pa"] - p["pb"])
            elif k in p["j"][2:]:
                if p["pb"] > p["pa"]: jg += 1
                dif += (p["pb"] - p["pa"])
        final.append({"Maestro": nom, "JG": jg, "DIF": dif})
    st.table(pd.DataFrame(final).sort_values(["JG", "DIF"], ascending=False).reset_index(drop=True))
