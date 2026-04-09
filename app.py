import streamlit as st
import json
import os

# Pagina instellingen
st.set_page_config(page_title="EHBO Kennis-toets", page_icon="🚑")

def laad_vragen():
    if os.path.exists('vragen.json'):
        with open('vragen.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def bewaar_vraag(nieuwe_vraag):
    vragen = laad_vragen()
    vragen.append(nieuwe_vraag)
    with open('vragen.json', 'w', encoding='utf-8') as f:
        json.dump(vragen, f, indent=2, ensure_ascii=False)

# Navigatie
menu = ["Quiz doen", "Vraag toevoegen"]
keuze = st.sidebar.selectbox("Menu", menu)

if keuze == "Quiz doen":
    st.title("🚑 EHBO Diagnose Toets")
    vragen = laad_vragen()
    
    if not vragen:
        st.warning("Er zijn nog geen vragen geladen.")
    else:
        # Gebruik session_state om de voortgang bij te houden
        if 'vraag_nr' not in st.session_state:
            st.session_state.vraag_nr = 0
            st.session_state.score = 0

        if st.session_state.vraag_nr < len(vragen):
            v = vragen[st.session_state.vraag_nr]
            st.subheader(f"Vraag {st.session_state.vraag_nr + 1}")
            st.write(v["v"])

            if v["type"] == "mc":
                antwoord = st.radio("Kies de juiste diagnose:", v["o"], key=f"q_{st.session_state.vraag_nr}")
                if st.button("Bevestig"):
                    if antwoord == v["a"]:
                        st.success(f"Correct! {v['u']}")
                        st.session_state.score += 1
                    else:
                        st.error(f"Onjuist. Het was: {v['a']}. {v['u']}")
                    st.session_state.vraag_nr += 1
                    st.button("Volgende vraag")
            
            else: # Checkbox type
                st.write("Selecteer alle symptomen die hierbij horen:")
                gekozen = []
                for optie in v["o"]:
                    if st.checkbox(optie, key=f"ch_{optie}_{st.session_state.vraag_nr}"):
                        gekozen.append(optie)
                
                if st.button("Bevestig"):
                    if sorted(gekozen) == sorted(v["a"]):
                        st.success(f"Correct! {v['u']}")
                        st.session_state.score += 1
                    else:
                        st.error(f"Onjuist. De juiste symptomen zijn: {', '.join(v['a'])}. {v['u']}")
                    st.session_state.vraag_nr += 1
                    st.button("Volgende vraag")
        else:
            st.balloons()
            st.success(f"Toets afgerond! Je score: {st.session_state.score}/{len(vragen)}")
            if st.button("Opnieuw starten"):
                st.session_state.vraag_nr = 0
                st.session_state.score = 0
                st.rerun()

elif keuze == "Vraag toevoegen":
    st.title("➕ Nieuwe vraag beheren")
    with st.form("vraag_form"):
        type_v = st.selectbox("Type", ["mc", "check"])
        vraag = st.text_input("Vraag of Diagnose")
        opties = st.text_input("Opties (komma-gescheiden)")
        antwoord = st.text_input("Antwoord(en) (bij meerdere: komma-gescheiden)")
        uitleg = st.text_area("Uitleg")
        
        if st.form_submit_button("Opslaan"):
            nieuwe_v = {
                "type": type_v,
                "v": vraag,
                "o": [o.strip() for o in opties.split(",")],
                "a": [a.strip() for a in antwoord.split(",")] if type_v == "check" else antwoord,
                "u": uitleg
            }
            bewaar_vraag(nieuwe_v)
            st.success("Vraag toegevoegd!")
