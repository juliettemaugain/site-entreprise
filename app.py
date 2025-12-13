import streamlit as st

# 1. Config PRO
st.set_page_config(
    page_title="Outils Viticoles - Laurent Miquel",
    page_icon="🍇",
    layout="wide"
)

# 2. CSS pour cacher le menu hamburger inutile en haut à droite et styliser
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; color: #4F091D; text-align: center; font-family: 'Helvetica', sans-serif;}
    .sub-header {font-size: 1.5rem; color: gray; text-align: center; margin-bottom: 2rem;}
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 3. En-tête (Header) avec Logos/Titres
col_logo, col_titre, col_vide = st.columns([1, 4, 1])

with col_logo:
    # Si tu as un logo, décommente la ligne ci-dessous :
    # st.image("images/logo.png", width=120) 
    st.write("") # Espace vide si pas de logo

with col_titre:
    st.markdown("<h1 class='main-header'>DOMAINE LAURENT MIQUEL</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>CHÂTEAU CAZAL VIEL<br>Plateforme Technique Viticole</p>", unsafe_allow_html=True)

st.divider()

# 4. Belle image d'accueil (Bannière)
# Si tu n'as pas d'image, tu peux supprimer ces 3 lignes
try:
    st.image("images/banniere_domaine.jpg", use_container_width=True)
except:
    pass # Si l'image n'est pas là, on ne fait rien

# 5. Tableau de bord (Accès rapides)
st.markdown("### 🚀 Accès Rapides aux Outils")

col1, col2 = st.columns(2)

with col1:
    # On simule une "Carte" cliquable
    with st.container(border=True):
        st.markdown("### 🍇 Simulateurs")
        st.markdown("Outils de calculs de rendements et prévisions.")
        st.info("👉 **Accéder au simulateur** (via le menu à gauche)")

with col2:
    with st.container(border=True):
        st.markdown("### 📚 Documentation")
        st.markdown("Base de connaissances, fiches techniques et tutoriels.")
        st.success("👉 **Consulter les fiches** (via le menu à gauche)")

st.divider()

# 6. Actualités ou Message du moment (Optionnel)
st.subheader("📢 Notes de service / Actualités")
st.warning("""
**Campagne 2025** : Pensez à mettre à jour vos estimations de manquants avant la fin du mois.
""")