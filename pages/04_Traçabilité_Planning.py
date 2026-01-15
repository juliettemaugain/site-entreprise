import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Pilotage & Traçabilité")

st.title("🍇 Pilotage du Vignoble - La Gauphine")

# --- 1. DONNÉES RÉELLES (INTEGRATION DU TABLEAU COMPLET) ---

# Code couleur basé sur ton image (Cépage)
COLOR_MAP = {
    "Viognier": "blue",       # Bleu/Cyan
    "Chardonnay": "orange",   # Jaune/Orange
    "Syrah": "red",           # Rouge
    "Grenache": "darkred",    # Pourpre/Rouge foncé
    "Marselan": "purple",     # Violet
    "Merlot": "darkblue",
    "Caladoc": "pink"
}

# BASE DE DONNÉES PARCELLES
# J'ai regroupé les "1 et 2" (ex: Olivette) en additionnant les surfaces
DATA_PARCELLES = {
    # --- VIOGNIER (Bleu) ---
    "VIGA03": {"nom": "Vio Fournic bas JL", "cepage": "Viognier", "surface": 2.28, "annee": 1997, "lat": 43.4210, "lon": 3.0810},
    "VIGA01": {"nom": "Vio Jeune JL", "cepage": "Viognier", "surface": 2.70, "annee": 2001, "lat": 43.4225, "lon": 3.0830},
    "VIGA04": {"nom": "Vio Plantier JL", "cepage": "Viognier", "surface": 2.54, "annee": 2014, "lat": 43.4205, "lon": 3.0850},
    "VIGA_PL": {"nom": "La Plaine", "cepage": "Viognier", "surface": 2.50, "annee": 2015, "lat": 43.4230, "lon": 3.0860}, # Simulé
    "VIGA_TR": {"nom": "Travers", "cepage": "Viognier", "surface": 1.90, "annee": 2010, "lat": 43.4195, "lon": 3.0880}, # Simulé

    # --- CHARDONNAY (Jaune/Orange) ---
    "CHGA04": {"nom": "Chardo 11 & 12", "cepage": "Chardonnay", "surface": 7.06, "annee": 2011, "lat": 43.4190, "lon": 3.0800}, # Somme approx
    "CH_OLI": {"nom": "Olivette (Global)", "cepage": "Chardonnay", "surface": 3.33, "annee": 2018, "lat": 43.4180, "lon": 3.0790}, # Fusion Olivette 1 & 2

    # --- SYRAH (Rouge) ---
    "SYCA01": {"nom": "Syrah Plantier", "cepage": "Syrah", "surface": 1.50, "annee": 1999, "lat": 43.4240, "lon": 3.0820},
    "SYCA02": {"nom": "Syrah Puech", "cepage": "Syrah", "surface": 2.10, "annee": 2005, "lat": 43.4250, "lon": 3.0840},
    "SYCA03": {"nom": "Syrah Vigne", "cepage": "Syrah", "surface": 3.00, "annee": 2008, "lat": 43.4260, "lon": 3.0815},

    # --- GRENACHE (Pourpre) ---
    "GRCA01": {"nom": "Grenache Coste", "cepage": "Grenache", "surface": 1.85, "annee": 2002, "lat": 43.4215, "lon": 3.0780},
    
    # --- MARSELAN (Violet) ---
    "MACA01": {"nom": "Marselan", "cepage": "Marselan", "surface": 1.20, "annee": 2019, "lat": 43.4200, "lon": 3.0760},
}

# Calcul automatique de l'âge et attribution couleur
annee_actuelle = datetime.now().year
for code, data in DATA_PARCELLES.items():
    data["age"] = annee_actuelle - data["annee"]
    data["color"] = COLOR_MAP.get(data["cepage"], "gray") # Gris si cépage inconnu

# PLANNING ITK (Généré automatiquement pour l'exemple sur TOUTES les parcelles)
data_itk_list = []
for code in DATA_PARCELLES.keys():
    # On ajoute des tâches types viticoles
    data_itk_list.extend([
        {"parcelle_id": code, "tache": "Taille", "start": "2025-12-01", "end": "2026-02-28", "statut": "En cours"},
        {"parcelle_id": code, "tache": "Entretien Sol", "start": "2026-03-10", "end": "2026-03-25", "statut": "A faire"},
        {"parcelle_id": code, "tache": "Traitements", "start": "2026-05-01", "end": "2026-07-15", "statut": "Planifié"},
        {"parcelle_id": code, "tache": "Vendanges", "start": "2026-08-20", "end": "2026-09-15", "statut": "Planifié"},
    ])

df_itk = pd.DataFrame(data_itk_list)


# --- 2. INTERFACE : LA CARTE (EN HAUT) ---
st.subheader("🗺️ Carte du Vignoble Interactif")

# Colonnes pour Légende à droite de la carte
col_map, col_legend = st.columns([5, 1])

with col_map:
    # Centrage automatique
    avg_lat = sum([d['lat'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    avg_lon = sum([d['lon'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)
    
    # Ajout de la couche Satellite (Google Maps ou Esri) pour que tu te repères mieux
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=False,
        control=True
    ).add_to(m)

    # Ajout des marqueurs
    for code, info in DATA_PARCELLES.items():
        folium.Marker(
            [info["lat"], info["lon"]],
            popup=f"<b>{info['nom']}</b><br>{info['surface']} ha",
            tooltip=f"{info['nom']}",
            icon=folium.Icon(color=info["color"], icon="leaf", prefix="fa")
        ).add_to(m)

    map_output = st_folium(m, height=500, use_container_width=True)

with col_legend:
    st.markdown("### Légende")
    for cepage, color in COLOR_MAP.items():
        # Petite pastille de couleur en HTML
        st.markdown(f"<span style='color:{color};'>●</span> {cepage}", unsafe_allow_html=True)


# --- 3. INTERFACE : DÉTAILS & TRAÇABILITÉ (EN BAS) ---
selected_code = None

if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    for code, info in DATA_PARCELLES.items():
        # Tolérance de clic
        if abs(info["lat"] - lat_clic) < 0.0001:
            selected_code = code
            break

if selected_code:
    parcelle = DATA_PARCELLES[selected_code]
    
    st.divider()
    
    # En-tête de la fiche parcelle
    c_titre, c_kpi = st.columns([1, 3])
    with c_titre:
        st.markdown(f"## {parcelle['nom']}")
        st.caption(f"Code: {selected_code}")
    
    with c_kpi:
        k1, k2, k3 = st.columns(3)
        k1.metric("Surface", f"{parcelle['surface']} ha")
        k2.metric("Cépage", parcelle['cepage'], delta_color="off")
        k3.metric("Année Plantation", parcelle['annee'])

    # Section Planning
    st.subheader(f"🚜 Traçabilité & Planning : {parcelle['nom']}")
    
    df_filtered = df_itk[df_itk["parcelle_id"] == selected_code]
    
    if not df_filtered.empty:
        # Couleurs du Gantt
        colors_gantt = {
            "Fini": "#2ecc71", "En cours": "#3498db", 
            "A faire": "#f1c40f", "Planifié": "#95a5a6"
        }
        
        fig = px.timeline(
            df_filtered, 
            x_start="start", x_end="end", y="tache", color="statut",
            color_discrete_map=colors_gantt,
            title="Avancement de la campagne"
        )
        
        fig.update_yaxes(autorange="reversed", title="")
        fig.update_layout(height=300, xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
        
        # Petit tableau récapitulatif
        with st.expander("Voir les données brutes"):
            st.dataframe(df_filtered.drop(columns=["parcelle_id"]), use_container_width=True)
            
else:
    st.info("👆 Cliquez sur une parcelle de la carte pour afficher son carnet de plaine.")