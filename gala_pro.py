import streamlit as st
import pandas as pd
import urllib.parse
import json
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="GALA DE LOS 13 PRO", layout="wide")

# Estilos visuales de alta gama
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1e293b; border-radius: 8px; padding: 8px 16px; color: #94a3b8;
    }
    .stTabs [aria-selected="true"] { background-color: #38bdf8 !important; color: white !important; }
    
    /* Diseño de las Mesas (Inspirado en tu Excel) */
    .mesa-container {
        display: grid; grid-template-columns: 1fr 1.5fr 1fr; grid-template-rows: 1fr 1.2fr 1fr;
        gap: 10px; width: 280px; height: 220px; margin: 15px auto; text-align: center;
    }
    .pos-label { padding: 8px; border-radius: 6px; font-weight: bold; font-size: 13px; color: white; display: flex; align-items: center; justify-content: center; }
    .purple { background-color: #6b21a8; border: 1px solid #a855f7; } 
    .green { background-color: #065f46; border: 1px solid #10b981; }
    .mesa-center { 
        grid-column: 2; grid-row: 2; background: #334155; border: 2px dashed #fbbf24;
        border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fbbf24; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. SISTEMA DE ACCESO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🏆 Gala de los 13")
        clave = st.text_input("Ingrese su Clave de Acceso", type="password")
        if clave == "1234": # Aquí puedes cambiar tu clave
            st.session_state.autenticado = True
            st.rerun()
        elif clave != "":
            st.error("Clave incorrecta")
    st.stop()

# --- 3. LÓGICA DE DATOS (Memoria en tiempo real) ---
FILE_MEMORIA = "memoria_torneo.json"

def cargar_datos():
    if os.path.exists(FILE_MEMORIA):
        with open(FILE_MEMORIA, "r") as f:
            return json.load(f)
    return {"puntos": [], "nombres": {f"j{i}": f"Maestro {i}" for i in range(1, 14)}}

def guardar_datos(datos):
    with open(FILE_MEMORIA, "w") as f:
        json.dump(datos, f)

datos_globales = cargar_datos()

# --- 4. ROTACIÓN MAESTRA (13 Jugadores) ---
def obtener_ronda(r):
    # Tu combinación perfecta de 13 rondas
    rondas = {
        1:  {"desc": "j13", "m1": ["j1", "j12", "j8", "j5"], "m2": ["j2", "j11", "j3", "j10"], "m3": ["j4", "j9", "j6", "j7"]},
        2:  {"desc": "j1",  "m1": ["j2", "j13", "j9", "j6"], "m2": ["j3", "j12", "j4", "j11"], "m3": ["j5", "j10", "j7", "j8"]},
        3:  {"desc": "j2",  "m1": ["j3", "j1", "j10", "j7"], "m2": ["j4", "j13", "j5", "j12"], "m3": ["j6", "j11", "j8", "j9"]},
        4:  {"desc": "j3",  "m1": ["j4", "j2", "j11", "j8"], "m2": ["j5", "j1", "j6", "j13"], "m3": ["j7", "j12", "j9", "j10"]},
        5:  {"desc": "j4",  "m1": ["j5", "j3", "j12", "j9"], "m2": ["j6", "j2", "j7", "j1"], "m3": ["j8", "j13", "j10", "j11"]},
        6:  {"desc": "j5",  "m1": ["j6", "j4", "j13", "j10"], "m2": ["j7", "j3", "j8", "j2"], "m3": ["j9", "j1", "j11", "j12"]},
        7:  {"desc": "j6",  "m1": ["j7", "j5", "j1", "j11"], "m2": ["j8", "j4", "j9", "j3"], "m3": ["j10", "j2", "j12", "j13"]},
        8:  {"desc": "j7",  "m1": ["j8", "j6", "j2", "j12"], "m2": ["j9", "j5", "j10", "j4"], "m3": ["j11", "j3", "j13", "j1"]},
        9:  {"desc": "j8",  "m1": ["j9", "j7", "j3", "j13"], "m2": ["j10", "j6", "j11", "j5"], "m3": ["j12", "j4", "j1", "j2"]},
        10: {"desc": "j9",  "m1": ["j10", "j8", "j4", "j1"], "m2": ["j11", "j7", "j12", "j6"], "m3": ["j13", "j5", "j2", "j3"]},
        11: {"desc": "j10", "m1": ["j11", "j9", "j5", "j2"], "m2": ["j12", "j8", "j13", "j7"], "m3": ["j1", "j6", "j3", "j4"]},
        12: {"desc": "j11", "m1": ["j12", "j10", "j6", "j3"], "m2": ["j13", "j9", "j1", "j8"], "m3": ["j2", "j7", "j4", "j5"]},
        13: {"desc": "j12", "m1": ["j13", "j11", "j7", "j4"], "m2": ["j1", "j10", "j2", "j9"], "m3": ["j3", "j8", "j5", "j6"]},
    }
    return rondas.get(r)

# --- 5. INTERFAZ PRINCIPAL ---
with st.sidebar:
    st.header("⚙️ Configuración")
    for i in range(1, 14):
        key = f"j{i}"
        datos_globales["nombres"][key] = st.text_input(f"P{i}", datos_globales["nombres"][key])
    
    if st.button("💾 Guardar Nombres"):
        guardar_datos(datos_globales)
        st.success("Nombres actualizados")

r_actual = st.select_slider("RONDA ACTUAL", options=list(range(1, 14)))
d = obtener_ronda(r_actual)
n = datos_globales["nombres"]

tabs = st.tabs(["📝 CARGA", "🖼️ MESAS (SOLO LECTURA)", "📊 POSICIONES"])

with tabs[0]:
    st.info(f"🧘 Reposo: {n[d['desc']]}")
    def cargar_puntos(num, jug):
        st.subheader(f"MESA {num}")
        c1, c2 = st.columns(2)
        p_a = c1.number_input(f"Pareja {n[jug[0]]}/{n[jug[1]]}", 0, 200, key=f"p_a_{r_actual}_{num}")
        p_b = c2.number_input(f"Pareja {n[jug[2]]}/{n[jug[3]]}", 0, 200, key=f"p_b_{r_actual}_{num}")
        return {"r": r_actual, "m": num, "j1": jug[0], "j2": jug[1], "pa": p_a, "j3": jug[2], "j4": jug[3], "pb": p_b}

    res1 = cargar_puntos(1, d["m1"])
    res2 = cargar_puntos(2, d["m2"])
    res3 = cargar_puntos(3, d["m3"])

    if st.button("🔔 REGISTRAR PUNTOS DE ESTA RONDA"):
        # Limpiar ronda previa si existe y agregar nueva
        datos_globales["puntos"] = [p for p in datos_globales["puntos"] if p["r"] != r_actual]
        datos_globales["puntos"].extend([res1, res2, res3])
        guardar_datos(datos_globales)
        st.success("Resultados sincronizados")

with tabs[1]:
    st.subheader(f"Distribución Visual - Ronda {r_actual}")
    def dibujar_mesa(num, jug):
        st.markdown(f"""
        <div class="mesa-container">
            <div class="pos-label purple" style="grid-column: 2; grid-row: 1;">{n[jug[1]]}</div>
            <div class="pos-label green" style="grid-column: 1; grid-row: 2;">{n[jug[0]]}</div>
            <div class="mesa-center">MESA {num}</div>
            <div class="pos-label green" style="grid-column: 3; grid-row: 2;">{n[jug[2]]}</div>
            <div class="pos-label purple" style="grid-column: 2; grid-row: 3;">{n[jug[3]]}</div>
        </div>
        """, unsafe_allow_html=True)

    colA, colB, colC = st.columns(3)
    with colA: dibujar_mesa(1, d["m1"])
    with colB: dibujar_mesa(2, d["m2"])
    with colC: dibujar_mesa(3, d["m3"])

with tabs[2]:
    puntos_df = pd.DataFrame(datos_globales["puntos"])
    if not puntos_df.empty:
        stats = []
        for key, nombre in n.items():
            cA = puntos_df[(puntos_df['j1'] == key) | (puntos_df['j2'] == key)]
            cB = puntos_df[(puntos_df['j3'] == key) | (puntos_df['j4'] == key)]
            jg = len(cA[cA['pa'] > cA['pb']]) + len(cB[cB['pb'] > cA['pa']])
            pf = cA['pa'].sum() + cB['pb'].sum()
            pc = cA['pb'].sum() + cB['pa'].sum()
            stats.append({'Maestro': nombre, 'JG': jg, 'DIF': pf - pc})
        
        ranking = pd.DataFrame(stats).sort_values(by=['JG', 'DIF'], ascending=False).reset_index(drop=True)
        ranking.index += 1
        st.table(ranking)
        
        # EL BOOM: WhatsApp
        texto_wa = "🏆 *REPORTE GALA DE LOS 13*\n\n"
        for i, row in ranking.iterrows():
            medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
            texto_wa += f"{medalla} {i}. {row['Maestro']} (JG:{row['JG']}, DIF:{row['DIF']})\n"
        
        url_wa = f"https://wa.me/?text={urllib.parse.quote(texto_wa)}"
        st.markdown(f'<a href="{url_wa}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 ENVIAR POSICIONES A WHATSAPP</button></a>', unsafe_allow_html=True)
