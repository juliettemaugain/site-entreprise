import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Pilotage & Traçabilité")

st.title("🍇 Pilotage du Vignoble - La Gauphine")

# --- 1. DONNÉES RÉELLES (EXTRAITES DE TES IMAGES) ---

# Dictionnaire des couleurs par cépage (inspiré de ton Excel)
COLOR_MAP = {
    "Viognier": "blue",
    "Chardonnay": "orange", # Jaune est peu visible sur une carte, orange est mieux
    "Syrah": "red",
    "Grenache": "darkred"
}

# Tes Parcelles (J'ai simulé les coordonnées GPS exactes autour de Cessenon/Cazouls)
DATA_PARCELLES = {
    "VIGA03": {
        "nom": "Vio Fournic bas JL", 
        "cepage": "Viognier", 
        "surface": 2.2800, 
        "annee": 1997, 
        "cadastre": "C959, C960",
        "lat": 43.4210, "lon": 3.0810 
    },
    "VIGA01": {
        "nom": "Vio Jeune JL", 
        "cepage": "Viognier", 
        "surface": 2.7032, 
        "annee": 2001, 
        "cadastre": "C1938",
        "lat": 43.4225, "lon": 3.0830 
    },
    "VIGA04": {
        "nom": "Vio Plantier JL", 
        "cepage": "Viognier", 
        "surface": 2.5400, 
        "annee": 2014, 
        "cadastre": "C1947...",
        "lat": 43.4205, "lon": 3.0850 
    },
    "CHGA041": {
        "nom": "Chardo 11", 
        "cepage": "Chardonnay", 
        "surface": 2.5300, 
        "annee": 2011, 
        "cadastre": "C953...",
        "lat": 43.4190, "lon": 3.0800 
    },
    "CHGA042": {
        "nom": "Chardo 12", 
        "cepage": "Chardonnay", 
        "surface": 4.5345, 
        "annee": 2012, 
        "cadastre": "C955...",
        "lat": 43.4185, "lon": 3.0820 
    },
}

# Enrichissement automatique des données (Couleurs, Age...)
annee_actuelle = datetime.now().year
for code, data in DATA_PARCELLES.items():
    data["age"] = annee_actuelle - data["annee"]
    data["color"] = COLOR_MAP.get(data["cepage"], "gray")

# Planning ITK (Reconstitué pour la campagne 2026)
# J'ai mis des dates types pour la région.
data_itk_list = []
for code in DATA_PARCELLES.keys():
    # Tâches communes à toutes les parcelles pour l'exemple
    data_itk_list.extend([
        {"parcelle_id": code, "tache": "Taille d'hiver", "start": "2025-12-01", "end": "2026-02-15", "statut": "En cours"},
        {"parcelle_id": code, "tache": "Broyage Sarments", "start": "2026-02-20", "end": "2026-03-01", "statut": "A faire"},
        {"parcelle_id": code, "tache": "Entretien du sol (Méca)", "start": "2026-03-15", "end": "2026-04-01", "statut": "A faire"},
        {"parcelle_id": code, "tache": "Ebourgeonnage", "start": "2026-04-15", "end": "2026-05-05", "statut": "Planifié"},
        {"parcelle_id": code, "tache": "Traitements (Mildiou/Oïdium)", "start": "2026-05-10", "end": "2026-07-30", "statut": "Planifié"},
        {"parcelle_id": code, "tache": "Vendanges", "start": "2026-08-25", "end": "2026-09-10", "statut": "Planifié"},
    ])

df_itk = pd.DataFrame(data_itk_list)


# --- 2. INTERFACE : LA CARTE (EN HAUT) ---
st.subheader("🗺️ Carte du Vignoble")

col_map, col_legend = st.columns([4, 1])

with col_map:
    # Centrage automatique sur la moyenne des points
    avg_lat = sum([d['lat'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    avg_lon = sum([d['lon'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)

    # Ajout des parcelles
    for code, info in DATA_PARCELLES.items():
        folium.Marker(
            [info["lat"], info["lon"]],
            popup=f"<b>{info['nom']}</b><br>{info['cepage']}",
            tooltip=f"{code} - {info['cepage']}",
            icon=folium.Icon(color=info["color"], icon="leaf", prefix="fa")
        ).add_to(m)

    map_output = st_folium(m, height=450, use_container_width=True)

with col_legend:
    st.write("**Légende :**")
    st.caption(f"🔵 Viognier")
    st.caption(f"🟠 Chardonnay")
    st.caption(f"🔴 Syrah (Exemple)")


# --- 3. INTERFACE : LES DÉTAILS (EN DESSOUS) ---
selected_code = None

# Détection du clic sur la carte
if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    # On retrouve la parcelle par sa latitude (méthode simple)
    for code, info in DATA_PARCELLES.items():
        # On compare avec une petite marge d'erreur car les floats sont capricieux
        if abs(info["lat"] - lat_clic) < 0.0001:
            selected_code = code
            break

if selected_code:
    parcelle = DATA_PARCELLES[selected_code]
    
    st.divider()
    st.markdown(f"### 🍇 {parcelle['nom']} <span style='font-size:0.7em; color:gray'>({selected_code})</span>", unsafe_allow_html=True)
    
    # 1. Cartouche d'identité
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Surface", f"{parcelle['surface']} ha")
    c2.metric("Cépage", parcelle['cepage'], delta_color="off")
    c3.metric("Age de la vigne", f"{parcelle['age']} ans", help=f"Plantée en {parcelle['annee']}")
    c4.metric("Cadastre", parcelle['cadastre'])
    
    # 2. Planning
    st.subheader(f"📅 Calendrier des travaux 2026")
    
    df_filtered = df_itk[df_itk["parcelle_id"] == selected_code]
    
    if not df_filtered.empty:
        # Configuration des couleurs du GANTT
        colors_gantt = {
            "Fini": "#2ecc71",      # Vert
            "En cours": "#3498db",  # Bleu
            "A faire": "#f1c40f",   # Jaune/Orange
            "Planifié": "#95a5a6"   # Gris
        }
        
        fig = px.timeline(
            df_filtered, 
            x_start="start", x_end="end", y="tache", color="statut",
            color_discrete_map=colors_gantt,
            category_orders={"statut": ["Fini", "En cours", "A faire", "Planifié"]}
        )
        
        fig.update_yaxes(autorange="reversed", title="") # Ordre chrono
        fig.update_layout(
            xaxis_title="",
            height=350,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("Pas d'itinéraire technique défini pour cette parcelle.")
        
else:
    st.info("👆 Cliquez sur un marqueur bleu ou orange sur la carte pour voir le détail de la parcelle.")