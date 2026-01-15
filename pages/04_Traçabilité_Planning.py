import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, date

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Pilotage & Traçabilité")

st.title("🍇 Pilotage du Vignoble - La Gauphine")

# --- 1. DONNÉES (STATIQUES) ---

COLOR_MAP = {
    "Viognier": "blue", "Chardonnay": "orange", "Syrah": "red",
    "Grenache": "darkred", "Marselan": "purple", "Merlot": "darkblue", "Caladoc": "pink"
}

# Tes Parcelles (Statique)
DATA_PARCELLES = {
    "VIGA03": {"nom": "Vio Fournic bas JL", "cepage": "Viognier", "surface": 2.28, "annee": 1997, "lat": 43.4210, "lon": 3.0810},
    "VIGA01": {"nom": "Vio Jeune JL", "cepage": "Viognier", "surface": 2.70, "annee": 2001, "lat": 43.4225, "lon": 3.0830},
    "VIGA04": {"nom": "Vio Plantier JL", "cepage": "Viognier", "surface": 2.54, "annee": 2014, "lat": 43.4205, "lon": 3.0850},
    "VIGA_PL": {"nom": "La Plaine", "cepage": "Viognier", "surface": 2.50, "annee": 2015, "lat": 43.4230, "lon": 3.0860},
    "VIGA_TR": {"nom": "Travers", "cepage": "Viognier", "surface": 1.90, "annee": 2010, "lat": 43.4195, "lon": 3.0880},
    "CHGA04": {"nom": "Chardo 11 & 12", "cepage": "Chardonnay", "surface": 7.06, "annee": 2011, "lat": 43.4190, "lon": 3.0800},
    "CH_OLI": {"nom": "Olivette (Global)", "cepage": "Chardonnay", "surface": 3.33, "annee": 2018, "lat": 43.4180, "lon": 3.0790},
    "SYCA01": {"nom": "Syrah Plantier", "cepage": "Syrah", "surface": 1.50, "annee": 1999, "lat": 43.4240, "lon": 3.0820},
    "SYCA02": {"nom": "Syrah Puech", "cepage": "Syrah", "surface": 2.10, "annee": 2005, "lat": 43.4250, "lon": 3.0840},
    "SYCA03": {"nom": "Syrah Vigne", "cepage": "Syrah", "surface": 3.00, "annee": 2008, "lat": 43.4260, "lon": 3.0815},
    "GRCA01": {"nom": "Grenache Coste", "cepage": "Grenache", "surface": 1.85, "annee": 2002, "lat": 43.4215, "lon": 3.0780},
    "MACA01": {"nom": "Marselan", "cepage": "Marselan", "surface": 1.20, "annee": 2019, "lat": 43.4200, "lon": 3.0760},
}

# Calcul age/couleur
annee_actuelle = datetime.now().year
for code, data in DATA_PARCELLES.items():
    data["age"] = annee_actuelle - data["annee"]
    data["color"] = COLOR_MAP.get(data["cepage"], "gray")

# --- 2. GESTION DES DONNÉES ITK (DYNAMIQUE AVEC MÉMOIRE) ---

# On initialise la "mémoire" (session_state) si elle est vide
if "db_itk" not in st.session_state:
    # On crée la liste de départ (comme avant)
    initial_data = []
    for code in DATA_PARCELLES.keys():
        initial_data.extend([
            {"parcelle_id": code, "tache": "Taille", "start": date(2025, 12, 1), "end": date(2026, 2, 28), "statut": "En cours"},
            {"parcelle_id": code, "tache": "Entretien Sol", "start": date(2026, 3, 10), "end": date(2026, 3, 25), "statut": "A faire"},
        ])
    st.session_state.db_itk = initial_data

# On transforme la mémoire en DataFrame pour l'affichage
df_itk = pd.DataFrame(st.session_state.db_itk)
# Conversion des dates pour être sûr que Plotly comprenne
df_itk["start"] = pd.to_datetime(df_itk["start"])
df_itk["end"] = pd.to_datetime(df_itk["end"])


# --- 3. INTERFACE : LA CARTE ---
st.subheader("🗺️ Carte du Vignoble")

col_map, col_legend = st.columns([5, 1])

with col_map:
    avg_lat = sum([d['lat'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    avg_lon = sum([d['lon'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri', name='Esri Satellite', overlay=False, control=True
    ).add_to(m)

    for code, info in DATA_PARCELLES.items():
        folium.Marker(
            [info["lat"], info["lon"]],
            popup=f"<b>{info['nom']}</b>",
            icon=folium.Icon(color=info["color"], icon="leaf", prefix="fa")
        ).add_to(m)

    map_output = st_folium(m, height=450, use_container_width=True)

with col_legend:
    st.markdown("### Légende")
    for cepage, color in COLOR_MAP.items():
        st.markdown(f"<span style='color:{color};'>●</span> {cepage}", unsafe_allow_html=True)


# --- 4. DÉTAILS & AJOUT DE TÂCHE ---
selected_code = None

if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    for code, info in DATA_PARCELLES.items():
        if abs(info["lat"] - lat_clic) < 0.0001:
            selected_code = code
            break

if selected_code:
    parcelle = DATA_PARCELLES[selected_code]
    st.divider()
    
    # En-tête
    st.markdown(f"## {parcelle['nom']} ({parcelle['cepage']})")
    
    # SECTION 1 : VISUALISATION
    df_filtered = df_itk[df_itk["parcelle_id"] == selected_code]
    
    if not df_filtered.empty:
        colors_gantt = {"Fini": "#2ecc71", "En cours": "#3498db", "A faire": "#f1c40f", "Planifié": "#95a5a6"}
        fig = px.timeline(
            df_filtered, x_start="start", x_end="end", y="tache", color="statut",
            color_discrete_map=colors_gantt
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune tâche.")

    # SECTION 2 : FORMULAIRE D'AJOUT
    st.markdown("### 🚜 Saisir une nouvelle intervention")
    
    # On met le formulaire dans un cadre coloré ou un expander
    with st.expander("➕ Cliquer pour ajouter une tâche", expanded=True):
        with st.form(key="add_task_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_task_name = st.text_input("Nom de l'opération", placeholder="Ex: Rognage, Traitement...")
                new_status = st.selectbox("Statut", ["Planifié", "A faire", "En cours", "Fini"])
            with c2:
                d1 = st.date_input("Date de début", date.today())
                d2 = st.date_input("Date de fin", date.today())
            
            submit_btn = st.form_submit_button("Enregistrer l'intervention")
            
            if submit_btn:
                # Création du dictionnaire de la nouvelle tâche
                new_entry = {
                    "parcelle_id": selected_code,
                    "tache": new_task_name,
                    "start": d1,
                    "end": d2,
                    "statut": new_status
                }
                
                # AJOUT À LA MÉMOIRE DE SESSION
                st.session_state.db_itk.append(new_entry)
                
                # Message de succès et rechargement pour voir la modif
                st.success("Tâche ajoutée avec succès !")
                st.rerun()

else:
    st.info("Sélectionnez une parcelle sur la carte pour voir ou ajouter des travaux.")