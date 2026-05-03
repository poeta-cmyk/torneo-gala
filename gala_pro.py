import streamlit as st
import pandas as pd
import json
import os
import time
import urllib.parse

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

# --- 3. ESTILOS Y PANTALLA ROJA ---
st.markdown("""
    <style>
    .mesa-container { display: grid; grid-template-columns: 1fr 1.5fr 1fr; grid-template-rows: 1fr 1.2fr 1fr; gap: 5px; width: 280px; height: 200px; margin: 10px auto; text-align: center; }
    .pos-label { padding: 5px; border-radius: 5px; font-weight: bold; font-size: 13px; color: white; display: flex; align-items: center; justify-content: center; min-height: 40px; }
    .p-morada { background-color: #6b21a8; border: 1px solid #a855f7; } 
    .p-verde { background-color: #065f46; border: 1px solid #10b981; }
    .m-centro { grid-column: 2; grid-row: 2; background: #334155; border: 2px dashed #fbbf24; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fbbf24; font-weight: bold; }
    
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
        font-size: 70px;
        text-align: center;
        font-weight: 900;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. LÓGICA DEL TEMPORIZADOR ---
if 'end_time' not in st.session_state: st.session_state.end_time = None
if 'aviso_5min' not in st.session_state: st.session_state.aviso_5min = False

vencido = False
if st.session_state.end_time:
    segundos_restantes = st.session_state.end_time - time.time()
    if segundos_restantes <= 0:
        vencido = True
    elif segundos_restantes <= 300 and not st.session_state.aviso_5min:
        st.toast("⚠️ ¡ALERTA! QUEDAN 5 MINUTOS", icon="🔔")
        st.session_state.aviso_5min = True

# PANTALLA DE BLOQUEO POR TIEMPO
if vencido:
    st.markdown('<div class="overlay-rojo"><div class="texto-vencido">TIEMPO<br>VENCIDO</div></div>', unsafe_allow_html=True)
    if st.button("🔄 REINICIAR CRONÓMETRO"):
        st.session_state.end_time = None
        st.session_state.aviso_5min = False
        st.rerun()
    st.stop()

# --- 5. ENTRADA ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h2 style='text-align: center;'>🏆 Gala de los 13</h2>", unsafe_allow_html=True)
        clave = st.text_input("Clave:", type="password")
        if clave == "poeta1208":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown("### ⏳ Control de Tiempo")
    col_a, col_b = st.columns(2)
    if col_a.button("▶️ Iniciar"):
        st.session_state.end_time = time.time() + 35 * 60
        st.session_state.aviso_5min = False
        st.rerun()
    if col_b.button("⏱️ Reset"):
        st.session_state.end_time = None
        st.session_state.aviso_5min = False
        st.rerun()

    if st.session_state.end_time:
        m, s = divmod(int(st.session_state.end_time - time.time()), 60)
        st.markdown(f"<h2 style='text-align: center; color: #fbbf24;'>{m:02d}:{s:02d}</h2>", unsafe_allow_html=True)
        time.sleep(1)
        st.rerun()
    
    st.divider()
    for i in range(1, 14):
        k = f"j{i}"
        st.session_state.db["nombres"][k] = st.text_input(f"ID {i}", st.session_state.db["nombres"][k], key=f"s_{k}")
    if st.button("💾 Guardar Maestros"):
        with open(FILE, "w") as f: json.dump(st.session_state.db, f)

# --- 7. TABS PRINCIPALES ---
t1, t2, t3 = st.tabs(["📝 REGISTRO", "🖼️ MESAS", "📊 RANKING"])

with t1:
    r_sel = st.select_slider("RONDA ACTUAL", options=list(range(1, 14)))
    
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

    rd, noms = get_ronda(r_sel), st.session_state.db["nombres"]
    st.info(f"Maestro Libre: {noms[rd['desc']]}")
    
    def fila_puntos(n_m, ids):
        st.markdown(f"**MESA {n_m}**")
        cx, cy = st.columns(2)
        px = cx.number_input(f"Morados", 0, 200, key=f"r{r_sel}m{n_m}x")
        py = cy.number_input(f"Verdes", 0, 200, key=f"r{r_sel}m{n_m}y")
        return {"r": r_sel, "p_m": px, "p_v": py, "ids_m": ids[:2], "ids_v": ids[2:]}
    
    r_data = [fila_puntos(1, rd["m1"]), fila_puntos(2, rd["m2"]), fila_puntos(3, rd["m3"])]
    if st.button("🔔 Guardar Ronda", use_container_width=True):
        st.session_state.db["puntos"] = [p for p in st.session_state.db["puntos"] if p["r"] != r_sel]
        st.session_state.db["puntos"].extend(r_data)
        with open(FILE, "w") as f: json.dump(st.session_state.db, f)
        st.success("¡Datos guardados!")

with t2:
    def dibujar_mesa(n_m, ids):
        st.markdown(f'''<div class="mesa-container"><div class="pos-label p-morada" style="grid-column:2; grid-row:1;">{noms[ids[0]]}</div><div class="pos-label p-verde" style="grid-column:3; grid-row:2;">{noms[ids[3]]}</div><div class="m-centro">M {n_m}</div><div class="pos-label p-morada" style="grid-column:2; grid-row:3;">{noms[ids[1]]}</div><div class="pos-label p-verde" style="grid-column:1; grid-row:2;">{noms[ids[2]]}</div></div>''', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: dibujar_mesa(1, rd["m1"])
    with c2: dibujar_mesa(2, rd["m2"])
    with c3: dibujar_mesa(3, rd["m3"])

with t3:
    resumen = []
    for kid, n in noms.items():
        jg, pf, pc = 0, 0, 0
        for p in st.session_state.db.get("puntos", []):
            if kid in p["ids_m"]:
                pf += p["p_m"]; pc += p["p_v"]
                if p["p_m"] > p["p_v"]: jg += 1
            elif kid in p["ids_v"]:
                pf += p["p_v"]; pc += p["p_m"]
                if p["p_v"] > p["p_m"]: jg += 1
        resumen.append({"Maestro": n, "JG": jg, "DIF": pf - pc, "PC": pc})

    df = pd.DataFrame(resumen).sort_values(by=['JG', 'DIF', 'PC'], ascending=[False, False, True]).reset_index(drop=True)
    df.index += 1
    st.table(df)

    st.divider()
    txt_wa = f"*🏆 GALA DE LOS 13 - RESULTADOS*\n\n"
    for i, row in df.iterrows():
        txt_wa += f"*{i}. {row['Maestro']}*: {row['JG']}JG | {row['DIF']}DIF\n"
    
    st.link_button("📤 WhatsApp", f"https://wa.me/?text={urllib.parse.quote(txt_wa)}", use_container_width=True)
