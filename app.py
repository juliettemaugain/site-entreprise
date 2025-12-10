import streamlit as st
from PIL import Image

# 1. Configuration de la page (Doit être la première commande Streamlit)
st.set_page_config(
    page_title="Mon Portfolio Pro",
    page_icon="🍇",
    layout="wide"  # Utilise toute la largeur de l'écran
)

# 2. Barre latérale (Sidebar) pour les infos fixes
with st.sidebar:
    st.header("À propos")
    st.info(
        """
        Ce site regroupe mes outils de simulation et mes fiches techniques 
        pour la gestion viticole et agricole.
        """
    )
    st.markdown("---")
    st.markdown("📧 **Contact :** ton-email@pro.com")
    st.markdown("🔗 **LinkedIn :** [Ton Profil](https://www.linkedin.com)")

# 3. Corps principal - Section Présentation
col1, col2 = st.columns([3, 1]) # La colonne texte est 3x plus large que la colonne photo

with col1:
    st.title("Bienvenue sur mon Espace Pro 👋")
    st.markdown("""
    ### Ingénierie & Solutions Digitales
    Bonjour ! Je suis **[Ton Prénom]**, passionné par l'alliance entre l'agronomie et la technologie.
    
    J'ai créé cette plateforme pour centraliser mes travaux :
    * Des **simulateurs interactifs** pour l'aide à la décision.
    * Des **fiches techniques** numérisées et accessibles partout.
    * Des outils d'analyse de données.
    """)

with col2:
    # Si tu as une photo, décommente les 3 lignes ci-dessous :
    image = Image.open("images/profil.JPG") 
    st.image(image, width=200)
    
    # Sinon, on affiche une icône sympa en attendant
    st.markdown("# 🍇") 
    st.markdown("*(Simulateurs Viticoles)*")

st.divider()

# 4. Section : Ce que vous trouverez ici
st.header("🛠️ Mes Outils")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📊 Simulateurs")
    st.write("Des applications Python pour calculer vos rendements, gérer vos stocks ou analyser vos coûts.")
    st.success("👉 **À tester :** Le simulateur de rendements viticoles (voir menu à gauche)")

with col_b:
    st.subheader("📄 Fiches Techniques")
    st.write("Une base de connaissances accessible pour retrouver les itinéraires techniques et bonnes pratiques.")
    st.info("👉 **À lire :** Consultez la section documentation dans le menu.")

st.divider()

# 5. Pied de page
st.markdown(
    """
    <div style='text-align: center; color: grey;'>
        © 2024 - Développé avec Python & Streamlit par [Ton Nom]
    </div>
    """, 
    unsafe_allow_html=True
)