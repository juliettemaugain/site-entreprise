import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Simulateur de rendements viticoles", page_icon="🍷")

# Appliquer un style CSS global avec police Lato
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Lato', sans-serif;
    }
    .title {
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    .result-table td {
        padding: 5px 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Titre
st.markdown("<h1 class='title'>Simulateur de rendement viticole 🍷</h1>", unsafe_allow_html=True)
st.markdown("<p class='title'>Château Cazal Viel</p>", unsafe_allow_html=True)


# --- PARAMÈTRES ---
st.header("Paramètres")

parcelle = st.text_input("Nom de la parcelle")

# 1. Dictionnaire des cépages et poids
cepages_data = {
    "Albarino": 170, "Cabernet Franc": 160, "Cabernet Sauvignon": 150,
    "Carignan": 250, "Chardonnay": 190, "Cinsault": 300, 
    "Colombard": 190, "Grenache blanc": 250, "Grenache noir": 260, 
    "Marselan": 140, "Merlot": 190, "Mourvèdre": 210, 
    "Roussanne": 160, "Sauvignon Blanc": 150, "Syrah": 150, "Viognier": 210
}

# 2. Création de la liste triée + Ajout de "Autre"
liste_noms = sorted(list(cepages_data.keys()))
liste_noms.append("Autre (Saisie manuelle)")

choix_cepage = st.selectbox("Cépage", liste_noms)

# 3. Logique pour gérer le choix
if choix_cepage == "Autre (Saisie manuelle)":
    # Si c'est Autre, on demande le nom et on ne met pas de poids par défaut
    cepage_nom_final = st.text_input("Nom du cépage personnalisé", "Nouveau Cépage")
    poids_defaut = 0.0
else:
    # Si c'est un cépage connu, on prend son poids
    cepage_nom_final = choix_cepage
    poids_defaut = float(cepages_data[choix_cepage])

# Le poids est modifiable dans tous les cas
poids_grappe_g = st.number_input("Poids moyen d'une grappe (g)", value=poids_defaut, step=1.0)
coef_vinif = st.number_input("Coefficient de vinification (kg/hl)", value=150)

# Calcul des pieds / ha
mode_pieds = st.radio("Mode de calcul des pieds/ha :", ["Saisie directe", "Calcul à partir des espacements"])

if mode_pieds == "Saisie directe":
    nb_pieds = st.number_input("Nombre de pieds à l'hectare", value=5000)
else:
    interrang = st.number_input("Inter-rang (m)", min_value=0.5, value=2.5)
    intercep = st.number_input("Inter-pied (m)", min_value=0.3, value=1.0)
    # Protection contre la division par zéro
    if interrang > 0 and intercep > 0:
        nb_pieds = round(10000 / (interrang * intercep))
    else:
        nb_pieds = 0
    st.markdown(f"**Pieds/ha calculés : {nb_pieds}**")


# --- NOMBRE DE GRAPPES (C'est ici qu'il y avait l'erreur de doublon) ---
st.subheader("Nombre de grappes par pied")
methode = st.radio("Méthode de saisie :", ["Tableau Excel (40 pieds)", "Moyenne directe"])

moyenne_grappes = 0.0

if methode == "Tableau Excel (40 pieds)":
    # Le tableau Excel
    default_data = {"Pied": list(range(1, 41)), "Nombre de grappes": [0]*40}
    df_input = pd.DataFrame(default_data)
    
    edited_df = st.data_editor(
        df_input,