with t3:
    # 1. CÁLCULO DEL RANKING (Igual que antes)
    stats = []
    for kid, n in noms.items():
        jg, pf, pc = 0, 0, 0
        for p in st.session_state.db["puntos"]:
            if kid in p["j"][:2]: pf += p["pa"]; pc += p["pb"]; jg += (1 if p["pa"] > p["pb"] else 0)
            elif kid in p["j"][2:]: pf += p["pb"]; pc += p["pa"]; jg += (1 if p["pb"] > p["pa"] else 0)
        stats.append({"Maestro": n, "JG": jg, "DIF": pf - pc, "PC": pc})

    df = pd.DataFrame(stats).sort_values(by=['JG', 'DIF', 'PC'], ascending=[False, False, True]).reset_index(drop=True)
    df.index += 1
    
    # 2. MOSTRAR TABLA
    st.table(df)

    # 3. BOTÓN PARA WHATSAPP
    st.divider()
    
    # Creamos el texto para el mensaje
    texto_wa = f"*🏆 GALA DE LOS 13 - RESULTADOS RONDA {r_sel}*\n\n"
    for i, row in df.iterrows():
        # Usamos medallas para los primeros 3
        medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
        texto_wa += f"{medalla} *{i}. {row['Maestro']}*: {row['JG']} JG | {row['DIF']} DIF | {row['PC']} PC\n"
    
    texto_wa += "\n_Generado por la Geometría del Sentimiento_"
    
    # Codificar para URL
    import urllib.parse
    msg_url = urllib.parse.quote(texto_wa)
    whatsapp_link = f"https://wa.me/?text={msg_url}"
    
    st.link_button("📤 Publicar Ranking en WhatsApp", whatsapp_link, use_container_width=True)
