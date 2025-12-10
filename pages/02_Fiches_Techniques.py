import streamlit as st

st.set_page_config(page_title="Documentation Technique", page_icon="📄")

st.title("📚 Documentation & Tutoriels")
st.markdown("Retrouvez ici les fiches techniques d'utilisation et de maintenance des outils et des vidéos.")

# Création de deux onglets pour organiser la page
tab_fiches, tab_videos = st.tabs(["📄 Fiches Techniques", "🎥 Vidéos Youtube"])

# --- ONGLET 1 : LES FICHES ---
with tab_fiches:
    st.header("Fiches Techniques Viticoles")
    
    # --- FICHE N°1 ---
    col1, col2 = st.columns([1, 2]) # Colonne image petite, colonne texte grande
    
    with col1:
        # Remplace par le nom exact de ton image dans le dossier assets
        # Si tu n'as pas encore mis l'image, laisse commenté ou mets une image test
        st.image("images/Intercep_utilisation.png", caption="Aperçu")
        st.info("🖼️ (Image de la fiche ici)") 

    with col2:
        st.subheader("Utilisation du matériel X")
        st.write("""
        Description rapide de cette fiche. Elle explique comment régler le matériel 
        pour optimiser le passage dans les rangs étroits.
        """)
        
        # Bouton de téléchargement du PDF
        # Pour que ça marche, il faut que le fichier existe dans le dossier 'assets'
with open("images/Intercep_utilisation.pdf", "rb") as pdf_file:
    st.download_button(    # <--- J'ai ajouté la parenthèse ouvrante ici
        label="⬇️ Télécharger la fiche (PDF)",
        data=pdf_file,
        file_name="Intercep_utilisation.pdf",  # Le nom que le fichier aura une fois téléchargé sur l'ordi du client
        mime="application/pdf"
    )   # <--- J'ai ajouté la parenthèse fermante ici
    st.write("*(Le bouton de téléchargement apparaîtra une fois le PDF ajouté)*")

    st.divider() # Ligne de séparation pour la prochaine fiche

    # --- FICHE N°2 (Tu peux copier-coller le bloc ci-dessus pour ajouter d'autres fiches) ---
    st.subheader("Autre Fiche Technique")
    st.write("Description de la deuxième fiche...")


# --- ONGLET 2 : LES VIDÉOS ---
with tab_videos:
    st.header("Démonstrations Vidéo")
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.subheader("Manipulation porteur pellenc")
        # Remplace par ton lien Youtube
        st.video("https://youtu.be/w02ZVEQuqYA")
        st.caption("Explication courte de la vidéo.")

    with col_v2:
        st.subheader("Maintenance tracteurs New Holland")
        # Remplace par ton lien Youtube
        st.video("https://youtu.be/XT799lE8uwA")
        st.caption("Explication courte de la vidéo.")