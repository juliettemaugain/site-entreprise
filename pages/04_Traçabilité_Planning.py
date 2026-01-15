import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, date

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Pilotage & Traçabilité")
st.title("🍇 Pilotage du Vignoble - La Gauphine")

# --- 1. DONNÉES (PARCELLES) ---
# Code couleur par cépage
COLOR_MAP = {
    "Viognier": "blue", "Chardonnay": "orange", "Syrah": "red",
    "Grenache": "darkred", "Marselan": "purple", "Merlot": "darkblue", "Caladoc": "pink"
}

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

# Calculs automatiques
annee_actuelle = datetime.now().year
for code, data in DATA_PARCELLES.items():
    data["age"] = annee_actuelle - data["annee"]
    data["color"] = COLOR_MAP.get(data["cepage"], "gray")


# --- 2. GESTION DES TÂCHES (ITK) ---

# Initialisation de la base de données en mémoire
if "db_itk" not in st.session_state:
    initial_data = []
    # On peuple avec des données par défaut enrichies
    for code in DATA_PARCELLES.keys():
        initial_data.extend([
            {
                "id": f"{code}_1", # ID unique pour retrouver la tâche
                "parcelle_id": code, 
                "tache": "Taille", 
                "categorie": "Manuelle",
                "start": date(2025, 12, 1), 
                "end": date(2026, 2, 28), 
                "statut": "En cours",
                "cadence": 0.5, # ha/j
                "jours_restants": 5,
                "materiel": "Sécateurs élec.",
                "color_hex": "#3498db" # Bleu par défaut
            },
            {
                "id": f"{code}_2",
                "parcelle_id": code, 
                "tache": "Entretien Sol", 
                "categorie": "Mécanique",
                "start": date(2026, 3, 10), 
                "end": date(2026, 3, 25), 
                "statut": "A faire",
                "cadence": 4.0,
                "jours_restants": 1,
                "materiel": "Tracteur + Interceps",
                "color_hex": "#f1c40f" # Jaune
            },
        ])
    st.session_state.db_itk = initial_data

# Fonction utilitaire pour sauvegarder
def save_db():
    # Ici, plus tard, on ajoutera le code pour écrire dans un fichier Excel
    pass 


# --- 3. INTERFACE CARTE (HAUT DE PAGE) ---
col_map, col_legend = st.columns([5, 1])

with col_map:
    # Centrage automatique
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

    map_output = st_folium(m, height=400, use_container_width=True)

with col_legend:
    st.markdown("**Légende**")
    for cepage, color in COLOR_MAP.items():
        st.markdown(f"<span style='color:{color};'>●</span> {cepage}", unsafe_allow_html=True)


# --- 4. DÉTAILS & GESTION (BAS DE PAGE) ---
selected_code = None # <--- C'est cette ligne qui manquait !

# On vérifie d'abord si on a cliqué sur la carte
if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    for code, info in DATA_PARCELLES.items():
        if abs(info["lat"] - lat_clic) < 0.0001:
            selected_code = code
            break

# Maintenant on peut vérifier si selected_code existe
if selected_code:
    parcelle = DATA_PARCELLES[selected_code]
    
    # --- EN-TÊTE PARCELLE ---
    st.divider()
    st.markdown(f"## {parcelle['nom']} <span style='font-size:0.6em; color:gray'>({parcelle['cepage']} - {parcelle['surface']} ha)</span>", unsafe_allow_html=True)

    # Préparation des données pour cette parcelle
    df_global = pd.DataFrame(st.session_state.db_itk)
    
    # --- SÉCURITÉ ANTI-BUG (Si pas de couleur définie) ---
    if "color_hex" not in df_global.columns:
        df_global["color_hex"] = "#3498db" # Bleu par défaut
    else:
        df_global["color_hex"] = df_global["color_hex"].fillna("#3498db")
    # ----------------------------------------------------

    # Conversion dates
    df_global["start"] = pd.to_datetime(df_global["start"])
    df_global["end"] = pd.to_datetime(df_global["end"])
    
    # Filtrer pour la parcelle active
    df_filtered = df_global[df_global["parcelle_id"] == selected_code].copy()

    # --- GRAPHIQUE GANTT ---
    if not df_filtered.empty:
        fig = px.timeline(
            df_filtered, 
            x_start="start", x_end="end", y="tache", 
            color="color_hex", 
            hover_data=["statut", "categorie", "materiel", "cadence"],
            title="Planning des interventions"
        )
        # Force l'utilisation des couleurs hexadécimales
        fig.update_traces(marker=dict(color=df_filtered["color_hex"])) 
        fig.update_yaxes(autorange="reversed", title="")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune intervention enregistrée.")

    # --- ONGLETS DE GESTION ---
    tab_add, tab_edit, tab_data = st.tabs(["➕ Nouvelle Tâche", "✏️ Modifier Tâche", "📊 Données Brutes"])

    # --- ONGLET 1 : AJOUTER ---
    with tab_add:
        with st.form("add_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_task = st.text_input("Nom de la tâche", placeholder="Ex: Rognage")
                new_cat = st.selectbox("Catégorie", ["Manuelle", "Mécanique", "Irrigation", "Autre"])
                new_mat = st.text_input("Matériel nécessaire", placeholder="Ex: Tracteur A + Atomiseur")
                new_color = st.color_picker("Couleur sur le planning", "#00f900")
            with c2:
                d1 = st.date_input("Début", date.today())
                d2 = st.date_input("Fin", date.today())
                new_status = st.selectbox("Statut", ["Planifié", "A faire", "En cours", "Fini"])
                sc1, sc2 = st.columns(2)
                new_cadence = sc1.number_input("Cadence (ha/j)", 0.0, 100.0, 1.0)
                new_rest = sc2.number_input("Jours restants est.", 0.0, 100.0, 1.0)

            if st.form_submit_button("Enregistrer"):
                new_entry = {
                    "id": f"{selected_code}_{datetime.now().timestamp()}",
                    "parcelle_id": selected_code,
                    "tache": new_task,
                    "categorie": new_cat,
                    "start": d1, "end": d2,
                    "statut": new_status,
                    "cadence": new_cadence,
                    "jours_restants": new_rest,
                    "materiel": new_mat,
                    "color_hex": new_color
                }
                st.session_state.db_itk.append(new_entry)
                st.success("Ajouté !")
                st.rerun()

    # --- ONGLET 2 : MODIFIER ---
    with tab_edit:
        if df_filtered.empty:
            st.write("Rien à modifier.")
        else:
            task_choice = st.selectbox("Sélectionner l'intervention à modifier :", df_filtered["tache"].unique())
            
            # Retrouver la ligne dans la base
            row_to_edit = None
            index_in_db = -1
            
            for idx, item in enumerate(st.session_state.db_itk):
                if item["parcelle_id"] == selected_code and item["tache"] == task_choice:
                    row_to_edit = item
                    index_in_db = idx
                    break
            
            if row_to_edit:
                with st.form("edit_form"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        # Index safe retrieval
                        l_statut = ["Planifié", "A faire", "En cours", "Fini"]
                        idx_statut = l_statut.index(row_to_edit["statut"]) if row_to_edit["statut"] in l_statut else 0
                        e_statut = st.selectbox("Statut", l_statut, index=idx_statut)
                        
                        l_cat = ["Manuelle", "Mécanique", "Irrigation", "Autre"]
                        cat_val = row_to_edit.get("categorie", "Autre")
                        idx_cat = l_cat.index(cat_val) if cat_val in l_cat else 3
                        e_cat = st.selectbox("Catégorie", l_cat, index=idx_cat)

                        e_mat = st.text_input("Matériel", value=row_to_edit.get("materiel", ""))
                        e_color = st.color_picker("Couleur", value=row_to_edit.get("color_hex", "#cccccc"))
                    
                    with col_b:
                        # Gestion dates safe
                        d_start = row_to_edit["start"]
                        if isinstance(d_start, pd.Timestamp): d_start = d_start.date()
                        
                        d_end = row_to_edit["end"]
                        if isinstance(d_end, pd.Timestamp): d_end = d_end.date()

                        e_d1 = st.date_input("Début", d_start)
                        e_d2 = st.date_input("Fin", d_end)
                        
                        ec1, ec2 = st.columns(2)
                        e_cadence = ec1.number_input("Cadence (ha/j)", value=float(row_to_edit.get("cadence", 0.0)))
                        e_rest = ec2.number_input("Jours restants", value=float(row_to_edit.get("jours_restants", 0.0)))

                    if st.form_submit_button("💾 Mettre à jour"):
                        st.session_state.db_itk[index_in_db].update({
                            "statut": e_statut, "categorie": e_cat, "materiel": e_mat,
                            "color_hex": e_color, "start": e_d1, "end": e_d2,
                            "cadence": e_cadence, "jours_restants": e_rest
                        })
                        st.success("Modification enregistrée !")
                        st.rerun()

    # --- ONGLET 3 : DATA ---
    with tab_data:
        st.dataframe(df_filtered)

else:
    st.info("👆 Cliquez sur une parcelle de la carte pour gérer les travaux.")