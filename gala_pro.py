import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="GALA 13", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    clave = st.text_input("Clave:", type="password")
    if clave == "poeta1208":
        st.session_state.auth = True
        st.rerun()
    st.stop()

def cargar():
    if os.path.exists("m.json"):
        with open("m.json", "r") as f: return json.load(f)
    return {"p": [], "n": {f"j{i}": f"Jugador {i}" for i in range(1, 14)}}

if 'd' not in st.session_state: st.session_state.d = cargar()

def rondas(r):
    return {
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
    }[r]

# Interfaz
r_sel = st.slider("Ronda", 1, 13)
rd = rondas(r_sel)
n = st.session_state.auth # solo para acortar

t1, t2 = st.tabs(["Carga", "Posiciones"])

with t1:
    st.write(f"Libre: {st.session_state.d['n'][rd['desc']]}")
    def mesa(id_m, j):
        st.write(f"Mesa {id_m}")
        c1, c2 = st.columns(2)
        v1 = c1.number_input(f"{st.session_state.d['n'][j[0]]}-{st.session_state.d['n'][j[1]]}", 0, 200, key=f"v1{r_sel}{id_m}")
        v2 = c2.number_input(f"{st.session_state.d['n'][j[2]]}-{st.session_state.d['n'][j[3]]}", 0, 200, key=f"v2{r_sel}{id_m}")
        return {"r": r_sel, "j": j, "v1": v1, "v2": v2}
    
    res = [mesa(1, rd['m1']), mesa(2, rd['m2']), mesa(3, rd['m3'])]
    if st.button("Guardar Ronda"):
        st.session_state.d["p"] = [x for x in st.session_state.d["p"] if x["r"] != r_sel]
        st.session_state.d["p"].extend(res)
        with open("m.json", "w") as f: json.dump(st.session_state.d, f)
        st.success("Guardado")

with t2:
    stats = []
    for k, nom in st.session_state.d["n"].items():
        jg, dif = 0, 0
        for p in st.session_state.d["p"]:
            if k in p["j"][:2]:
                if p["v1"] > p["v2"]: jg += 1
                dif += (p["v1"] - p["v2"])
            elif k in p["j"][2:]:
                if p["v2"] > p["v1"]: jg += 1
                dif += (p["v2"] - p["v1"])
        stats.append({"Nombre": nom, "JG": jg, "Dif": dif})
    st.table(pd.DataFrame(stats).sort_values(["JG", "Dif"], ascending=False))
