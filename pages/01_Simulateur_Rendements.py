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
    cepage_nom_final = st.text_input("Nom du cépage personnalisé", "Nouveau Cépage")
    poids_defaut = 0.0
else:
    cepage_nom_final = choix_cepage
    poids_defaut = float(cepages_data[choix_cepage])

poids_grappe_g = st.number_input("Poids moyen d'une grappe (g)", value=poids_defaut, step=1.0)
coef_vinif = st.number_input("Coefficient de vinification (kg/hl)", value=150)

# Calcul des pieds / ha
mode_pieds = st.radio("Mode de calcul des pieds/ha :", ["Saisie directe", "Calcul à partir des espacements"])

if mode_pieds == "Saisie directe":
    nb_pieds = st.number_input("Nombre de pieds à l'hectare", value=5000)
else:
    interrang = st.number_input("Inter-rang (m)", min_value=0.5, value=2.5)
    intercep = st.number_input("Inter-pied (m)", min_value=0.3, value=1.0)
    if interrang > 0 and intercep > 0:
        nb_pieds = round(10000 / (interrang * intercep))
    else:
        nb_pieds = 0
    st.markdown(f"**Pieds/ha calculés : {nb_pieds}**")

# --- NOMBRE DE GRAPPES ---
st.subheader("Nombre de grappes par pied")
methode = st.radio("Méthode de saisie :", ["Tableau Excel (nombre variable de pieds)", "Moyenne directe"])

moyenne_grappes = 0.0

if methode == "Tableau Excel (nombre variable de pieds)":
    # Sélection du nombre d'observations
    nb_observations = st.number_input(
        "Nombre d'observations (pieds à compter)",
        min_value=1,
        max_value=100,
        value=40,
        step=1
    )

    # Création du tableau dynamique
    default_data = {
        "Pied": list(range(1, nb_observations + 1)),
        "Nombre de grappes": [0] * nb_observations
    }
    df_input = pd.DataFrame(default_data)

    edited_df = st.data_editor(
        df_input,
        use_container_width=True,
        num_rows="fixed",
        hide_index=True,
        column_config={
            "Pied": st.column_config.NumberColumn(
                "Pied", width="small", disabled=True, format="%d"
            ),
            "Nombre de grappes": st.column_config.NumberColumn(
                "Nombre de grappes", min_value=0, step=1
            )
        }
    )
    moyenne_grappes = edited_df["Nombre de grappes"].mean()
    st.markdown(f"**Moyenne calculée : {moyenne_grappes:.2f} grappes/pied**")

else:
    moyenne_grappes = st.number_input(
        "Saisir la moyenne de grappes par pied",
        min_value=0.0,
        value=0.0,
        step=0.1,
        format="%.2f"
    )

# --- POURCENTAGES DE PERTES ---
manquants = st.number_input(
    "Pourcentage de pieds manquants (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=0.01,
    format="%.2f"
)

pertes = st.number_input(
    "Pourcentage de pertes à la récolte (%)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.01,
    format="%.2f"
)

# --- RÉSULTATS ---
st.subheader("Résultats")
if st.button("Calculer le rendement"):
    poids_kg = poids_grappe_g / 1000

    # Calculs
    rendement_t_ha = nb_pieds * moyenne_grappes * poids_kg * (1 - manquants/100) * (1 - pertes/100) / 1000

    if coef_vinif > 0:
        rendement_hl_ha = nb_pieds * moyenne_grappes * poids_kg * (1 - manquants/100) * (1 - pertes/100) / coef_vinif
    else:
        rendement_hl_ha = 0

    result = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Parcelle": parcelle,
        "Cépage": cepage_nom_final,
        "Poids grappe (g)": poids_grappe_g,
        "Grappes/pied": round(moyenne_grappes, 2),
        "Pieds/ha": nb_pieds,
        "% manquants": manquants,
        "% pertes": pertes,
        "t/ha": round(rendement_t_ha, 2),
        "hl/ha": round(rendement_hl_ha, 2)
    }

    st.markdown("### 📊 Résultats du calcul")
    with st.expander("Voir les détails", expanded=True):
        st.success(
            f"""
            - **Parcelle** : {parcelle or "Non précisé"}
            - **Cépage** : {cepage_nom_final}
            - **Grappes/pied** : {round(moyenne_grappes, 2)}
            - **Poids grappe** : {poids_grappe_g} g
            - **Pieds/ha** : {nb_pieds}
            - **Manquants** : {manquants} %
            - **Pertes** : {pertes} %
            ---
            - ✅ **Rendement estimé** : **{round(rendement_t_ha, 2)} t/ha**
            - 🍷 **Rendement vin estimé** : **{round(rendement_hl_ha, 2)} hl/ha**
            """
        )

    if "historique" not in st.session_state:
        st.session_state.historique = []
    st.session_state.historique.append(result)

# Historique
st.subheader("Historique des simulations 📊")
if "historique" in st.session_state and st.session_state.historique:
    df = pd.DataFrame(st.session_state.historique)
    st.dataframe(df)

    col1, col2 = st.columns(2)
    if col1.button("❌ Effacer dernier résultat"):
        st.session_state.historique.pop()
    if col2.button("🗑️ Effacer tout l'historique"):
        st.session_state.historique = []
else:
    st.info("Aucune simulation pour le moment.")
