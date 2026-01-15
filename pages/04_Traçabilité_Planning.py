import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Pilotage & Traçabilité")

st.title("🚜 Pilotage des Parcelles & ITK")

# --- 1. CRÉATION DES DONNÉES (Simulation de ta base de données) ---

# Liste des parcelles (Simulées)
DATA_PARCELLES = {
    "P1": {"nom": "Les Vignes du Nord", "surface": 5.4, "culture": "Vigne", "lat": 43.60, "lon": 3.88, "color": "green"},
    "P2": {"nom": "Le Champ du Moulin", "surface": 12.1, "culture": "Blé Tendre", "lat": 43.61, "lon": 3.90, "color": "orange"},
    "P3": {"nom": "Verger Sud", "surface": 3.2, "culture": "Pommes", "lat": 43.59, "lon": 3.87, "color": "red"},
}

# Liste des tâches ITK (Simulées)
# On imagine une liste de tâches avec dates, statuts, etc.
data_itk = [
    {"parcelle_id": "P1", "tache": "Taille", "start": "2024-01-10", "end": "2024-01-25", "statut": "Fini", "color": "green"},
    {"parcelle_id": "P1", "tache": "Fertilisation", "start": "2024-03-01", "end": "2024-03-05", "statut": "A faire", "color": "gray"},
    {"parcelle_id": "P2", "tache": "Semis", "start": "2023-10-15", "end": "2023-10-20", "statut": "Fini", "color": "green"},
    {"parcelle_id": "P2", "tache": "Fongicide T1", "start": "2024-04-10", "end": "2024-04-12", "statut": "En cours", "color": "blue"},
    {"parcelle_id": "P3", "tache": "Récolte", "start": "2024-09-01", "end": "2024-09-15", "statut": "Planifié", "color": "gray"},
]
df_itk = pd.DataFrame(data_itk)

# --- 2. INTERFACE : COLONNE GAUCHE (CARTE) / COLONNE DROITE (DÉTAILS) ---

col1, col2 = st.columns([1, 1.5]) # La colonne de droite est un peu plus large

with col1:
    st.subheader("🗺️ Vue Carte")
    st.info("Clique sur un marqueur pour voir les détails.")
    
    # Création de la carte centrée (ici sur une zone fictive sud France)
    m = folium.Map(location=[43.60, 3.89], zoom_start=13)

    # Ajout des marqueurs pour chaque parcelle
    for pid, info in DATA_PARCELLES.items():
        folium.Marker(
            [info["lat"], info["lon"]],
            popup=info["nom"],
            tooltip=info["nom"],
            # On utilise l'ID comme identifiant pour le clic
            icon=folium.Icon(color=info["color"], icon="leaf")
        ).add_to(m)

    # Affichage de la carte et récupération du clic
    # C'est ici que la magie opère : st_folium renvoie les infos de l'interaction
    map_output = st_folium(m, height=400, width="100%")

with col2:
    st.subheader("📋 Détails & Planning")

    # Logique de sélection
    selected_parcelle_id = None
    
    # On regarde si l'utilisateur a cliqué sur un marqueur
    if map_output["last_object_clicked"]:
        # On essaie de retrouver quelle parcelle correspond aux coordonnées cliquées
        lat_clic = map_output["last_object_clicked"]["lat"]
        # Recherche simple par latitude (pour l'exemple)
        for pid, info in DATA_PARCELLES.items():
            if info["lat"] == lat_clic:
                selected_parcelle_id = pid
                break
    
    # --- AFFICHAGE CONDITIONNEL ---
    if selected_parcelle_id:
        parcelle = DATA_PARCELLES[selected_parcelle_id]
        
        # 1. Cartouche d'infos (Metrics)
        c1, c2, c3 = st.columns(3)
        c1.metric("Nom", parcelle["nom"])
        c2.metric("Surface", f"{parcelle['surface']} ha")
        c3.metric("Culture", parcelle["culture"])
        
        st.divider()
        
        # 2. Planning GANTT (Filtré sur la parcelle sélectionnée)
        st.write(f"📅 **Calendrier ITK - {parcelle['nom']}**")
        
        # Filtrer le DataFrame pour ne garder que cette parcelle
        df_filtered = df_itk[df_itk["parcelle_id"] == selected_parcelle_id]
        
        if not df_filtered.empty:
            fig = px.timeline(
                df_filtered, 
                x_start="start", 
                x_end="end", 
                y="tache", 
                color="statut",
                title="Avancement des tâches",
                color_discrete_map={"Fini": "green", "En cours": "blue", "A faire": "gray", "Planifié": "lightgray"}
            )
            # Amélioration du look du Gantt
            fig.update_yaxes(autorange="reversed") # Tâches dans l'ordre chronologique
            st.plotly_chart(fig, use_container_width=True)
            
            # 3. Tableau de données brutes (facultatif mais utile)
            with st.expander("Voir les données brutes"):
                st.dataframe(df_filtered)
        else:
            st.warning("Aucune tâche planifiée pour cette parcelle.")
            
    else:
        st.write("👈 **Veuillez sélectionner une parcelle sur la carte pour voir son itinéraire technique.**")