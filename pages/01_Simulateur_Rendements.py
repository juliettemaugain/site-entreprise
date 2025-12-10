
import streamlit as st
import pandas as pd
from datetime import datetime

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

# Paramètres
st.header("Paramètres")

parcelle = st.text_input("Nom de la parcelle")

cepages = {
    "Colombard": 190, "Roussanne": 160, "Grenache blanc": 250, "Sauvignon Blanc": 150,
    "Viognier": 210, "Albarino": 170, "Chardonnay": 190, "Syrah": 150, "Marselan": 140,
    "Grenache noir": 260, "Cinsault": 300, "Cabernet Franc": 160, "Cabernet Sauvignon": 150,
    "Merlot": 190, "Mourvèdre": 210, "Carignan": 250
}
cepage = st.selectbox("Cépage", list(cepages.keys()))
poids_grappe_g = st.number_input("Poids moyen d'une grappe (g)", value=cepages[cepage])
coef_vinif = st.number_input("Coefficient de vinification (kg/hl)", value=150)

mode_pieds = st.radio("Mode de calcul des pieds/ha :", ["Saisie directe", "Calcul à partir des espacements"])
if mode_pieds == "Saisie directe":
    nb_pieds = st.number_input("Nombre de pieds à l'hectare", value=5000)
else:
    interrang = st.number_input("Inter-rang (m)", min_value=0.5, value=2.5)
    intercep = st.number_input("Inter-pied (m)", min_value=0.3, value=1.0)
    nb_pieds = round(10000 / (interrang * intercep))
    st.markdown(f"**Pieds/ha calculés : {nb_pieds}**")

# Choix de méthode
st.subheader("Nombre de grappes par pied")
methode = st.radio("Méthode de saisie :", ["Tableau Excel (40 pieds)", "Moyenne directe"])

moyenne_grappes = 0

if methode == "Tableau Excel (40 pieds)":
    default_data = {"Pied": list(range(1, 41)), "Nombre de grappes": [0]*40}
    df_input = pd.DataFrame(default_data)
    edited_df = st.data_editor(df_input, use_container_width=True, num_rows="fixed")
    moyenne_grappes = edited_df["Nombre de grappes"].mean()
    st.markdown(f"**Moyenne calculée : {moyenne_grappes:.2f} grappes/pied**")
else:
    moyenne_grappes = st.number_input("Moyenne de grappes par pied", min_value=0.0, step=0.1)

# Pourcentages
manquants = st.number_input(
    "Pourcentage de pieds manquants (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=0.01,  # Permet de monter de 0.01 en 0.01
    format="%.2f"  # Affiche bien deux décimales (ex: 12.50)
)
pertes = st.slider("Pourcentage de pertes possible à la récolte (%)", 0, 100, 5)

# Résultats
st.subheader("Résultats")
if st.button("Calculer le rendement"):
    poids_kg = poids_grappe_g / 1000
    rendement_t_ha = nb_pieds * moyenne_grappes * poids_kg * (1 - manquants/100) * (1 - pertes/100) / 1000
    rendement_hl_ha = nb_pieds * moyenne_grappes * poids_kg * (1 - manquants/100) * (1 - pertes/100) / coef_vinif

    result = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Parcelle": parcelle,
        "Cépage": cepage,
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
            - **Cépage** : {cepage}
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
    