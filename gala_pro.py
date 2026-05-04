with t1:
    r_sel = st.select_slider("RONDA ACTUAL", options=list(range(1, 14)))
    rd, noms = get_ronda(r_sel), st.session_state.db["nombres"]
    st.info(f"Maestro Libre: {noms[rd['desc']]}")
    
    # --- FUNCIÓN DE FILA MEJORADA ---
    def fila_res(n_m, ids):
        st.markdown(f"**MESA {n_m}**")
        
        # BUSCAR SI YA HAY DATOS GUARDADOS PARA ESTA RONDA Y MESA
        p_m_prev, p_v_prev = 0, 0
        for p in st.session_state.db.get("puntos", []):
            if p["r"] == r_sel:
                # Identificamos la mesa por el primer ID del equipo morado
                if p["ids_m"][0] == ids[0]: 
                    p_m_prev = p["p_m"]
                    p_v_prev = p["p_v"]
        
        c1, c2 = st.columns(2)
        # Cargamos el valor previo con el parámetro 'value'
        p1 = c1.number_input(f"Morados ({noms[ids[0]]} / {noms[ids[1]]})", 0, 200, value=p_m_prev, key=f"r{r_sel}m{n_m}m")
        p2 = c2.number_input(f"Verdes ({noms[ids[2]]} / {noms[ids[3]]})", 0, 200, value=p_v_prev, key=f"r{r_sel}m{n_m}v")
        
        return {"r": r_sel, "p_m": p1, "p_v": p2, "ids_m": ids[:2], "ids_v": ids[2:]}
    
    res_input = [fila_res(1, rd["m1"]), fila_res(2, rd["m2"]), fila_res(3, rd["m3"])]
    
    if st.button("💾 Guardar Ronda " + str(r_sel), use_container_width=True):
        # Eliminamos registros viejos de esta ronda para no duplicar
        st.session_state.db["puntos"] = [p for p in st.session_state.db["puntos"] if p["r"] != r_sel]
        # Agregamos los nuevos
        st.session_state.db["puntos"].extend(res_input)
        
        with open(FILE, "w") as f: 
            json.dump(st.session_state.db, f)
        
        st.balloons()
        st.success(f"¡Resultados de la Ronda {r_sel} asegurados!")
