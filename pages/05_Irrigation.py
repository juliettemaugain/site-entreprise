import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime, date
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Irrigation - Domaine Viticole", page_icon="💧")
st.title("💧 Gestion de l'Irrigation")

# --- CHEMINS DES FICHIERS ---
CSV_IRRIGATION = "data/irrigation_data.csv"
DATA_PARCELLES = st.session_state.get("DATA_PARCELLES", {})  # Récupère les données des parcelles depuis votre page existante

# --- COULEURS POUR LES ÉQUIPEMENTS ---
COLOR_EQUIPMENT = {
    "Vanne": "#3498db",      # Bleu
    "Filtre": "#e74c3c",     # Rouge
    "Pompe": "#2ecc71",      # Vert
    "Compteur": "#f39c12",   # Orange
    "Autre": "#9b59b6"       # Violet
}

STATUS_COLORS = {
    "OK": "#2ecc71",         # Vert
    "Maintenance": "#f39c12",# Orange
    "Panne": "#e74c3c"       # Rouge
}

# --- DONNÉES DES ÉQUIPEMENTS D'IRRIGATION (EXEMPLE) ---
@st.cache_data
def load_irrigation_data():
    # Si le fichier CSV existe, on le charge
    if os.path.exists(CSV_IRRIGATION):
        df = pd.read_csv(CSV_IRRIGATION)
        return df.to_dict("records")
    else:
        # Données par défaut (à remplacer par vos données réelles)
        return [
            {
                "id": "V_01",
                "nom": "Vanne Principale Secteur A",
                "type": "Vanne",
                "secteur": "DOMAINE PRINCIPAL",
                "parcelle": "P_00",  # Syrah Isabelle
                "lat": 43.4290,
                "lon": 3.0930,
                "status": "OK",
                "debit": 50.0,       # L/min
                "pression": 2.5,     # bar
                "derniere_maintenance": "2023-10-15",
                "prochaine_maintenance": "2024-04-15",
                "notes": "Vanne principale pour le secteur A"
            },
            {
                "id": "F_01",
                "nom": "Filtre Entrée Secteur B",
                "type": "Filtre",
                "secteur": "SECTEUR SAVIGNAC",
                "parcelle": "P_68",  # Viognier Haut Savignac
                "lat": 43.4175,
                "lon": 3.1167,
                "status": "Maintenance",
                "debit": 30.0,
                "pression": 1.8,
                "derniere_maintenance": "2023-11-20",
                "prochaine_maintenance": "2024-05-20",
                "notes": "Filtre à nettoyer tous les 3 mois"
            },
            # Ajoutez d'autres équipements ici...
        ]

# --- GÉNÉRATION DE LA CARTE ---
def generate_irrigation_map():
    # Créer une carte centrée sur le domaine
    m = folium.Map(location=[43.4260, 3.0900], zoom_start=14, tiles="CartoDB positron")

    # --- 1. AJOUTER LES SECTEURS (comme dans votre code existant) ---
    SECTEURS = {
        "SECTEUR GAUPHINE": [43.4025, 3.1155],
        "SECTEUR SAINTE LUCIE": [43.4405, 3.0735],
        "SECTEUR SAVIGNAC": [43.4180, 3.1230],
        "SECTEUR LA JASSE NEUVE": [43.4210, 3.0700],
        "DOMAINE PRINCIPAL": [43.4260, 3.0900]
    }

    for nom_secteur, coords in SECTEURS.items():
        folium.map.Marker(
            coords,
            icon=folium.DivIcon(
                icon_size=(300, 40),
                icon_anchor=(150, 20),
                html=f"""<div style="font-size: 18px; font-weight: 900; color: rgba(0,0,255,0.6); text-shadow: 2px 2px 10px rgba(0,0,0,0.8); text-align: center; text-transform: uppercase; letter-spacing: 3px;">{nom_secteur}</div>"""
            )
        ).add_to(m)

    # --- 2. AJOUTER LES PARCELLES (en transparence) ---
    for code, info in DATA_PARCELLES.items():
        if "geometry" in info:
            folium.GeoJson(
                info["geometry"],
                style_function=lambda x: {
                    'fillColor': "#cccccc",  # Gris clair
                    'color': "#aaaaaa",     # Gris foncé
                    'weight': 1,
                    'fillOpacity': 0.2      # Très transparent
                },
                tooltip=info["nom"]
            ).add_to(m)

    # --- 3. AJOUTER LES ÉQUIPEMENTS D'IRRIGATION ---
    equipments = load_irrigation_data()
    for eq in equipments:
        # Couleur en fonction du statut
        color = STATUS_COLORS.get(eq["status"], "#95a5a6")  # Gris par défaut

        # Popup HTML pour afficher les détails
        html_popup = f"""
        <div style="width: 250px; font-family: Arial, sans-serif;">
            <h4 style="margin-bottom: 5px; color: {COLOR_EQUIPMENT[eq['type']]};">{eq['type']} - {eq['nom']}</h4>
            <b>ID :</b> {eq['id']}<br>
            <b>Secteur :</b> {eq['secteur']}<br>
            <b>Parcelle :</b> {DATA_PARCELLES.get(eq['parcelle'], {}).get('nom', 'N/A')}<br>
            <hr style="margin: 8px 0; border-top: 1px solid #ccc;">
            <b>Statut :</b> <span style="color: {color};">{eq['status']}</span><br>
            <b>Débit :</b> {eq['debit']} L/min<br>
            <b>Pression :</b> {eq['pression']} bar<br>
            <b>Dernière maintenance :</b> {eq['derniere_maintenance']}<br>
            <b>Prochaine maintenance :</b> {eq['prochaine_maintenance']}<br>
            <hr style="margin: 8px 0; border-top: 1px solid #ccc;">
            <b>Notes :</b><br>
            <div style="font-size: 12px; color: #555;">{eq['notes']}</div>
        </div>
        """

        # Ajouter le marqueur
        folium.Marker(
            [eq["lat"], eq["lon"]],
            icon=folium.Icon(
                icon="tint",          # Icône "goutte d'eau"
                prefix="fa",          # Utilise Font Awesome
                color=color,
                icon_color="white"
            ),
            popup=folium.Popup(html_popup, max_width=300),
            tooltip=f"{eq['type']} - {eq['nom']} ({eq['status']})"
        ).add_to(m)

    return m

# --- 4. INTERFACE UTILISATEUR ---
# Colonnes pour la carte et les filtres
col_map, col_filters = st.columns([4, 1])

with col_filters:
    st.header("Filtres")
    equipments = load_irrigation_data()

    # Filtre par type
    types = ["Tous"] + sorted(list(set([eq["type"] for eq in equipments])))
    selected_type = st.selectbox("Type d'équipement", types)

    # Filtre par statut
    statuses = ["Tous"] + sorted(list(set([eq["status"] for eq in equipments])))
    selected_status = st.selectbox("Statut", statuses)

    # Filtre par secteur
    secteurs = ["Tous"] + sorted(list(set([eq["secteur"] for eq in equipments])))
    selected_secteur = st.selectbox("Secteur", secteurs)

    # Appliquer les filtres
    filtered_equipments = [
        eq for eq in equipments
        if (selected_type == "Tous" or eq["type"] == selected_type)
        and (selected_status == "Tous" or eq["status"] == selected_status)
        and (selected_secteur == "Tous" or eq["secteur"] == selected_secteur)
    ]

    # Afficher le nombre d'équipements filtrés
    st.markdown(f"**{len(filtered_equipments)} équipements** affichés")

    # Bouton pour exporter en CSV
    if st.button("Exporter les données"):
        df = pd.DataFrame(filtered_equipments)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger CSV",
            data=csv,
            file_name="equipements_irrigation.csv",
            mime="text/csv"
        )

with col_map:
    # Générer et afficher la carte
    m = generate_irrigation_map()
    map_output = st_folium(m, height=600, use_container_width=True)

    # Afficher les détails si un équipement est cliqué
    if map_output["last_object_clicked"]:
        clicked_lat = map_output["last_object_clicked"]["lat"]
        clicked_lon = map_output["last_object_clicked"]["lng"]

        # Trouver l'équipement le plus proche
        closest_eq = None
        min_dist = float('inf')

        for eq in filtered_equipments:
            dist = ((eq["lat"] - clicked_lat)**2 + (eq["lon"] - clicked_lon)**2)**0.5
            if dist < min_dist and dist < 0.002:  # Seuil de 200m
                min_dist = dist
                closest_eq = eq

        if closest_eq:
            st.subheader(f"Détails : {closest_eq['nom']}")
            st.markdown(f"""
            - **Type** : {closest_eq['type']}
            - **Secteur** : {closest_eq['secteur']}
            - **Parcelle** : {DATA_PARCELLES.get(closest_eq['parcelle'], {}).get('nom', 'N/A')}
            - **Statut** : <span style="color: {STATUS_COLORS[closest_eq['status']]};">{closest_eq['status']}</span>
            - **Débit** : {closest_eq['debit']} L/min
            - **Pression** : {closest_eq['pression']} bar
            - **Dernière maintenance** : {closest_eq['derniere_maintenance']}
            - **Prochaine maintenance** : {closest_eq['prochaine_maintenance']}
            """, unsafe_allow_html=True)

            st.text_area("Notes", closest_eq["notes"], height=100)

            # Bouton pour signaler un problème
            if st.button("Signaler un problème", key=f"problem_{closest_eq['id']}"):
                st.warning("Fonctionnalité à implémenter : notification par email ou ticket de maintenance")

# --- LÉGENDE ---
st.sidebar.markdown("### Légende")
for eq_type, color in COLOR_EQUIPMENT.items():
    st.sidebar.markdown(f"<span style='color:{color};'>■</span> {eq_type}", unsafe_allow_html=True)

st.sidebar.markdown("---")
for status, color in STATUS_COLORS.items():
    st.sidebar.markdown(f"<span style='color:{color};'>●</span> {status}", unsafe_allow_html=True)
