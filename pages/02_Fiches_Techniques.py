import streamlit as st

st.set_page_config(page_title="Documentation Technique", page_icon="📚", layout="wide")

st.title("📚 Documentation Technique")

# --- BARRE DE RECHERCHE ---
# Permet de filtrer les fiches si tu en as 20 !
recherche = st.text_input("🔍 Rechercher une fiche...", "")

# --- 1. TA BASE DE DONNÉES ---
# C'est ici que tu ajoutes tes 20 fiches. 
# Tu as juste à copier-coller une ligne entre les accolades {} et changer les noms.
fiches = [
    {
        "titre": "Utilisation Intercep",
        "image": "images/intercep_utilisation.png",
        "pdf": "images/intercep.pdf"
    },
    {
        "titre": "Réglage Pulvérisateur",
       "image": "images/intercep_utilisation.png",
        "pdf": "images/intercep.pdf"      # Remplace par le bon PDF
    },
   
]

# --- 2. FILTRAGE ---
# Si on a écrit un truc dans la recherche, on ne garde que les fiches correspondantes
fiches_a_afficher = [f for f in fiches if recherche.lower() in f["titre"].lower()]

if not fiches_a_afficher:
    st.warning("Aucune fiche trouvée avec ce nom.")

# --- 3. AFFICHAGE EN GRILLE (GALERIE) ---
# On définit qu'on veut 3 colonnes (ou 4 si tu préfères)
cols = st.columns(3) 

for index, fiche in enumerate(fiches_a_afficher):
    # L'astuce mathématique pour remplir les colonnes une par une :
    # index % 3 vaudra 0, puis 1, puis 2, puis recommence à 0...
    colonne_actuelle = cols[index % 3]
    
    with colonne_actuelle:
        # On crée un cadre visuel (container) pour faire propre
        with st.container(border=True):
            st.subheader(fiche["titre"])
            
            # Affichage de l'image (l'aperçu)
            try:
                st.image(fiche["image"], use_container_width=True)
            except:
                st.error(f"Image introuvable : {fiche['image']}")

            # Bouton de téléchargement
            try:
                with open(fiche["pdf"], "rb") as pdf_file:
                    st.download_button(
                        label="⬇️ PDF",
                        data=pdf_file,
                        file_name=fiche["pdf"].split("/")[-1], # Garde juste le nom du fichier
                        mime="application/pdf",
                        use_container_width=True # Le bouton prend toute la largeur
                    )
            except:
                st.warning("PDF en attente")