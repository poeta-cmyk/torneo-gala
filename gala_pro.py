import streamlit as st
import pandas as pd
import json
import os

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

# --- 3. FLUJO DE ENTRADA (AUTENTICACIÓN + DECISIÓN) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'decidido' not in st.session_state:
    st.session_state.decidido = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><h2 style='text-align: center;'>🏆 Gala de los 13</h2>", unsafe_allow_html=True)
        clave = st.text_input("Introduce la clave para iniciar:", type="password", key="p_acceso")
        if clave == "poeta1208":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# Si ya entró pero no ha decidido si borrar o no
if not st.session_state.decidido:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #fbbf24;'>Poeta ¿Deseas hacer un Máster con 13 nuevos maestros?</h3>", unsafe_allow_html=True)
        st.write("")
        c_si, c_no = st.columns(2)
        
        if c_si.button("✅ SÍ (Empezar de cero)", use_container_width=True):
            # RESET TOTAL
            st.session_state.db = {"puntos": [], "nombres": {f"j{i}": f"Maestro {i}" for i in range(1, 14)}}
            with open(FILE, "w") as f: json.dump(st.session_state.db, f)
            st.session_state.decidido = True
            st.rerun()
            
        if c_no.button("❌ NO (Mantener nombres)", use_container_width=True):
            # SE QUEDA COMO ESTÁ
            st.session_state.decidido = True
            st.rerun()
    st.stop()

# --- 4. ESTILOS ---
st.markdown("""
    <style>
    .mesa-container { display: grid; grid-template-columns: 1fr 1.5fr 1fr; grid-template-rows: 1fr 1.2fr 1fr; gap: 5px; width: 280px; height: 200px; margin: 10px auto; text-align: center; }
    .pos-label { padding: 5px; border-radius: 5px; font-weight: bold; font-size: 13px; color: white; display: flex; align-items: center; justify-content: center; min-height: 40px; }
    .p-morada { background-color: #6b21a8; border: 1px solid #a855f7; } 
    .p-verde { background-color: #065f46; border: 1px solid #10b981; }
    .m-centro { grid-column: 2; grid-row: 2; background: #334155; border: 2px dashed #fbbf24; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fbbf24; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 5. LÓGICA DE RONDAS ---
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

# --- 6. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Maestros")
    for i in range(1, 14):
        k = f"j{i}"
        st.session_state.db["nombres"][k] = st.text_input(f"ID {i}", st.session_state.db["nombres"][k], key=f"side_{k}")
    if st.button("💾 Guardar"):
        with open(FILE, "w") as f: json.dump(st.session_state.db, f)

# --- 7. TABS PRINCIPALES ---
r_sel = st.select_slider("RONDA", options=list(range(1, 14)))
rd = get_ronda(r_sel)
noms = st.session_state.db["nombres"]

t1, t2, t3 = st.tabs(["📝 CARGA", "🖼️ MESAS", "📊 RANKING"])

with t1:
    st.info(f"Libre: {noms[rd['desc']]}")
    def fila_res(n_m, ids):
        st.markdown(f"**MESA {n_m}**")
        c1, c2 = st.columns(2)
        p1 = c1.number_input(f"{noms[ids[0]]}/{noms[ids[1]]}", 0, 200, key=f"r{r_sel}m{n_m}a")
        p2 = c2.number_input(f"{noms[ids[2]]}/{noms[ids[3]]}", 0, 200, key=f"r{r_sel}m{n_m}b")
        return {"r": r_sel, "j": ids, "pa": p1, "pb": p2}
    
    res = [fila_res(1, rd["m1"]), fila_res(2, rd["m2"]), fila_res(3, rd["m3"])]
    if st.button("🔔 Registrar"):
        st.session_state.db["puntos"] = [p for p in st.session_state.db["puntos"] if p["r"] != r_sel]
        st.session_state.db["puntos"].extend(res)
        with open(FILE, "w") as f: json.dump(st.session_state.db, f)
        st.balloons()

with t2:
    def dibujo(n_m, ids):
        st.markdown(f'''
            <div class="mesa-container">
                <div class="pos-label p-morada" style="grid-column:2; grid-row:1;">{noms[ids[0]]}</div>
                <div class="pos-label p-verde" style="grid-column:3; grid-row:2;">{noms[ids[3]]}</div>
                <div class="m-centro">M {n_m}</div>
                <div class="pos-label p-morada" style="grid-column:2; grid-row:3;">{noms[ids[1]]}</div>
                <div class="pos-label p-verde" style="grid-column:1; grid-row:2;">{noms[ids[2]]}</div>
            </div>
        ''', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: dibujo(1, rd["m1"])
    with c2: dibujo(2, rd["m2"])
    with c3: dibujo(3, rd["m3"])

with t3:
    ranking = []
    for k, n in noms.items():
        jg, dif = 0, 0
        for p in st.session_state.db["puntos"]:
            if k in p["j"][:2]:
                if p["pa"] > p["pb"]: jg += 1
                dif += (p["pa"] - p["pb"])
            elif k in p["j"][2:]:
                if p["pb"] > p["pa"]: jg += 1
                dif += (p["pb"] - p["pa"])
        ranking.append({"Maestro": n, "JG": jg, "DIF": dif})
    st.table(pd.DataFrame(ranking).sort_values(["JG", "DIF"], ascending=False).reset_index(drop=True))
