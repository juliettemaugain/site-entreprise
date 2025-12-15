import streamlit as st

st.set_page_config(page_title="Tutoriels Vidéo", page_icon="🎥", layout="wide")

st.title("🎥 Tutoriels & Démonstrations")
st.markdown("Retrouvez ici les vidéos explicatives sur l'utilisation et l'entretient du matériel.")

# --- TA BASE DE DONNÉES VIDÉOS ---
# C'est ici que tu ajoutes tes liens Youtube.
# Copie le bloc { ... } pour ajouter une nouvelle vidéo.
videos_db = [
    {
        "titre": "Manipulation du porteur Pellenc : de éole à la tête de récolte",
        "url": "https://youtu.be/w02ZVEQuqYA", # Remplace par ton lien
        "description": "Vidéo explicative de toutes les étapes à réaliser lors de cette manipulation, à faire dans l'autre sens pour remettre l'éole. Bien respecter les consignes de sécurités de base"
    },
    {
        "titre": "Maintenance tracteurs New Holland",
        "url": "https://youtu.be/XT799lE8uwA", # Remplace par ton lien
        "description": "Vidéo tutoriel courte pour rapeler les maintenances et graissages sur les tracteurs NeW Holland."
    },
    # Tu pourras ajouter d'autres vidéos ici plus tard...
]

st.divider()

# --- AFFICHAGE AUTOMATIQUE ---
# On crée 2 colonnes pour afficher les vidéos côte à côte
cols = st.columns(2)

for index, video in enumerate(videos_db):
    # Logique pour remplir les colonnes une par une
    colonne_actuelle = cols[index % 2]
    
    with colonne_actuelle:
        with st.container(border=True):
            st.subheader(video["titre"])
            
            # Le lecteur vidéo Youtube intégré
            st.video(video["url"])
            
            # La description en petit en dessous
            st.caption(video["description"])

# Un petit message si la liste est vide (au cas où)
if not videos_db:
    st.info("Aucune vidéo disponible pour le moment.")