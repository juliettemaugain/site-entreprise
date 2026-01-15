import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, date, timedelta

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Pilotage & Traçabilité")
st.title("🍇 Pilotage du Vignoble")

# --- 1. DONNÉES (PARCELLES) ---
COLOR_MAP = {
    "Viognier": "blue", "Chardonnay": "orange", "Syrah": "red",
    "Grenache": "darkred", "Marselan": "purple", "Merlot": "darkblue", "Caladoc": "pink"
}

DATA_PARCELLES = {
    # --- SYRAH ISABELLE (VIGA03) ---
    "VIGA03": {
        "nom": "Syrah Isabelle", "cepage": "Syrah", "surface": 0.56, "annee": 2019, # J'ai mis 2019 (age 7 ans)
        "lat": 43.4296, "lon": 3.0925,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [3.0924931192498377, 43.4296143369082],
                [3.092055089459109, 43.428945850119646],
                [3.0934897957306475, 43.428517092637975],
                [3.093604064371874, 43.42866001213599],
                [3.0935405817928086, 43.42876604896469],
                [3.093464402699169, 43.428844423892656],
                [3.0933628305733123, 43.428913578156795],
                [3.093242213674756, 43.428913578156795],
                [3.0931279450334728, 43.42893201928061],
                [3.092594691374927, 43.42958206530179],
                [3.0924931192498377, 43.4296143369082]
            ]]
        }
    },

   # --- DÉCOUPAGE DE "LA PLAINE" EN 5 PARCELLES DISTINCTES ---
    
    "VIGA_PL1": {
        "nom": "La Plaine 1 (Nord-Est)", "cepage": "Viognier", "surface": 0.50, "annee": 2015, 
        "lat": 43.4289, "lon": 3.0930, # Point central calculé
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [3.092493, 43.429614], [3.092055, 43.428946], [3.093490, 43.428517], 
                [3.093604, 43.428660], [3.093541, 43.428766], [3.093464, 43.428844], 
                [3.093363, 43.428914], [3.093242, 43.428914], [3.093128, 43.428932], 
                [3.092595, 43.429582], [3.092493, 43.429614]
            ]]
        }
    },

    "VIGA_PL2": {
        "nom": "La Plaine 2 (Centre)", "cepage": "Viognier", "surface": 0.50, "annee": 2015,
        "lat": 43.4280, "lon": 3.0915,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [3.091501, 43.429019], [3.091162, 43.428491], [3.091705, 43.428113], 
                [3.091867, 43.428020], [3.091113, 43.426822], [3.091776, 43.426797], 
                [3.092495, 43.426894], [3.092798, 43.427365], [3.093003, 43.427693], 
                [3.093447, 43.428450], [3.092072, 43.428886], [3.091501, 43.429019]
            ]]
        }
    },

    "VIGA_PL3": {
        "nom": "La Plaine 3 (Est)", "cepage": "Viognier", "surface": 0.50, "annee": 2015,
        "lat": 43.4280, "lon": 3.0938,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [3.094155, 43.428700], [3.093952, 43.428501], [3.093641, 43.428575], 
                [3.092930, 43.427353], [3.093673, 43.427178], [3.094435, 43.428640], 
                [3.094155, 43.428700]
            ]]
        }
    },

    "VIGA_PL4": {
        "nom": "La Plaine 4 (Ouest)", "cepage": "Viognier", "surface": 0.50, "annee": 2015,
        "lat": 43.4280, "lon": 3.0905,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [3.091457, 43.429064], [3.090289, 43.429451], [3.089769, 43.429290], 
                [3.090080, 43.428529], [3.089832, 43.428031], [3.090270, 43.426915], 
                [3.091108, 43.426837], [3.091832, 43.428013], [3.091146, 43.428492], 
                [3.091457, 43.429064]
            ]]
        }
    },

    "VIGA_PL5": {
        "nom": "La Plaine 5 (Sud-Ouest)", "cepage": "Viognier", "surface": 0.50, "annee": 2015,
        "lat": 43.4280, "lon": 3.0890,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [3.089321, 43.429010], [3.088299, 43.428567], [3.088895, 43.427018], 
                [3.090190, 43.426916], [3.089321, 43.429010]
            ]]
        }
    },
    }
# Calculs automatiques
annee_actuelle = datetime.now().year
for code, data in DATA_PARCELLES.items():
    data["age"] = annee_actuelle - data["annee"]
    data["color"] = COLOR_MAP.get(data["cepage"], "gray")


# --- 2. GESTION DES TÂCHES (ITK) ---
if "db_itk" not in st.session_state:
    initial_data = []
    for code in DATA_PARCELLES.keys():
        initial_data.extend([
            {
                "id": f"{code}_1",
                "parcelle_id": code, 
                "tache": "Taille", 
                "categorie": "Manuelle",
                "start": date(2025, 12, 1), 
                "end": date(2026, 2, 28), 
                "statut": "En cours",
                "cadence": 0.5,
                "jours_estimes": 5.0,
                "materiel": "Sécateurs élec.",
                "color_hex": "#3498db"
            }
        ])
    st.session_state.db_itk = initial_data


# --- 3. INTERFACE CARTE ---
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
        
        # 1. DESSIN DU CONTOUR (Format GeoJSON Direct)
        if "geometry" in info:
            folium.GeoJson(
                info["geometry"],
                style_function=lambda x, color=info["color"]: {
                    'fillColor': color,
                    'color': color,
                    'weight': 2,
                    'fillOpacity': 0.4
                },
                tooltip=f"{info['nom']} ({info['surface']} ha)"
            ).add_to(m)

        # 2. DESSIN DU MARQUEUR (Toujours là pour cliquer)
        folium.Marker(
            [info["lat"], info["lon"]],
            popup=f"<b>{info['nom']}</b>",
            icon=folium.Icon(color=info["color"], icon="leaf", prefix="fa")
        ).add_to(m)

    map_output = st_folium(m, height=500, use_container_width=True)


# --- LOGIQUE DE SÉLECTION ---
selected_code_map = None
if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    for code, info in DATA_PARCELLES.items():
        if abs(info["lat"] - lat_clic) < 0.0001:
            selected_code_map = code
            break




# --- 5. ZONES D'ACTIONS (ONGLETS) ---
st.divider()
# ON AJOUTE L'ONGLET "STATISTIQUES" ICI
tab_view, tab_plan, tab_stats, tab_data = st.tabs(["🔍 Détail Parcelle", "🚜 Planification Groupée", "📊 Bilan & Stats", "🗃️ Données Brutes"])

# =========================================================
# ONGLET 1 : VUE DÉTAILLÉE (Code inchangé ou presque)
# =========================================================
with tab_view:
    if selected_code_map:
        parcelle = DATA_PARCELLES[selected_code_map]
        st.markdown(f"### 🍇 {parcelle['nom']} <span style='font-size:0.7em; color:gray'>({parcelle['cepage']} - {parcelle['surface']} ha)</span>", unsafe_allow_html=True)

        # Chargement
        df_global = pd.DataFrame(st.session_state.db_itk)
        required_cols = ["color_hex", "categorie", "materiel", "cadence", "jours_estimes", "statut"]
        for col in required_cols:
            if col not in df_global.columns: df_global[col] = None
            if col == "color_hex": df_global[col] = df_global[col].fillna("#3498db")
            elif col in ["cadence", "jours_estimes"]: df_global[col] = df_global[col].fillna(0.0)
            else: df_global[col] = df_global[col].fillna("-")
        
        df_global["start"] = pd.to_datetime(df_global["start"])
        df_global["end"] = pd.to_datetime(df_global["end"])
        
        df_filtered = df_global[df_global["parcelle_id"] == selected_code_map].copy()

        if not df_filtered.empty:
            color_map_gantt = {row["tache"]: row["color_hex"] for index, row in df_filtered.iterrows()}
            fig = px.timeline(
                df_filtered, 
                x_start="start", x_end="end", y="tache", 
                color="tache", color_discrete_map=color_map_gantt,
                hover_data=["statut", "categorie", "materiel", "jours_estimes"],
                title="Planning Parcelle"
            )
            fig.update_yaxes(autorange="reversed", title="")
            st.plotly_chart(fig, use_container_width=True)
            
            # Bouton suppression
            with st.expander("🗑️ Supprimer une tâche"):
                task_to_del = st.selectbox("Tâche à supprimer", df_filtered["tache"].unique(), key="del_select")
                if st.button("Confirmer suppression"):
                    st.session_state.db_itk = [
                        item for item in st.session_state.db_itk 
                        if not (item["parcelle_id"] == selected_code_map and item["tache"] == task_to_del)
                    ]
                    save_data()
                    st.success("Supprimé !")
                    st.rerun()
        else:
            st.info("Aucune intervention sur cette parcelle.")
    else:
        st.info("👆 Cliquez sur une parcelle de la carte pour voir son détail.")


# =========================================================
# ONGLET 2 : PLANIFICATION (Code inchangé)
# =========================================================
with tab_plan:
    st.subheader("🛠️ Ajouter une intervention (Groupée)")
    col_gauche, col_droite = st.columns([1, 2])
    
    with col_gauche:
        st.markdown("##### 1. Paramètres")
        default_selection = [selected_code_map] if selected_code_map else []
        selected_parcels_ids = st.multiselect("Parcelles :", options=DATA_PARCELLES.keys(), default=default_selection, format_func=lambda x: DATA_PARCELLES[x]['nom'])
        surface_totale = sum([DATA_PARCELLES[pid]['surface'] for pid in selected_parcels_ids])
        st.caption(f"Surface Totale : {surface_totale:.2f} ha")
        st.write("---")
        cadence_input = st.number_input("Cadence (h/ha)", 0.1, 100.0, 10.0, step=0.5)
        nb_personnes = st.number_input("Nb Personnes", 1, 50, 1)
        heures_totales = surface_totale * cadence_input
        jours_estimes_calc = heures_totales / (nb_personnes * 6)
        st.info(f"⏳ **{jours_estimes_calc:.1f} jours** (Total: {heures_totales:.1f} h)")

    with col_droite:
        st.markdown("##### 2. Détails")
        with st.form("bulk_add_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_task_name = st.text_input("Nom", placeholder="Ex: Ebourgeonnage")
                new_cat = st.selectbox("Catégorie", ["Manuelle", "Mécanique", "Traitements", "Récolte"])
                new_color = st.color_picker("Couleur", "#2ecc71")
            with c2:
                new_mat = st.text_input("Matériel")
                new_status = st.selectbox("Statut", ["Planifié", "A faire", "En cours", "Fini"])
            d_col1, d_col2 = st.columns(2)
            start_date = d_col1.date_input("Début", date.today())
            suggested_end = start_date + timedelta(days=int(jours_estimes_calc) if jours_estimes_calc >= 1 else 1)
            end_date = d_col2.date_input("Fin", value=suggested_end)
            
            if st.form_submit_button("✅ Valider"):
                if not selected_parcels_ids:
                    st.error("Sélectionnez une parcelle.")
                else:
                    timestamp_id = datetime.now().timestamp()
                    for pid in selected_parcels_ids:
                        new_entry = {
                            "id": f"{pid}_{timestamp_id}", "parcelle_id": pid,
                            "tache": new_task_name, "categorie": new_cat,
                            "start": start_date, "end": end_date, "statut": new_status,
                            "cadence": cadence_input, "jours_estimes": jours_estimes_calc,
                            "materiel": new_mat, "color_hex": new_color
                        }
                        st.session_state.db_itk.append(new_entry)
                    save_data()
                    st.success(f"Ajouté sur {len(selected_parcels_ids)} parcelles !")
                    st.rerun()


# =========================================================
# ONGLET 3 : STATISTIQUES (NOUVEAU !!!)
# =========================================================
with tab_stats:
    st.subheader("📊 Tableau de bord de la Campagne")
    
    # Préparation des données globales
    df_all = pd.DataFrame(st.session_state.db_itk)
    
    if df_all.empty:
        st.info("Pas assez de données pour afficher les statistiques.")
    else:
        # Sécurisation des données pour les calculs
        if "jours_estimes" not in df_all.columns: df_all["jours_estimes"] = 0.0
        df_all["jours_estimes"] = df_all["jours_estimes"].fillna(0.0).astype(float)
        # On ajoute le nom du cépage dans le tableau des tâches pour pouvoir trier par cépage
        df_all["cepage"] = df_all["parcelle_id"].apply(lambda x: DATA_PARCELLES[x]["cepage"] if x in DATA_PARCELLES else "Inconnu")

        # --- LIGNE 1 : KPI (Indicateurs Clés) ---
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        # Total Jours Hommes (Somme de tous les jours estimés)
        total_jours = df_all["jours_estimes"].sum()
        # Nombre d'interventions
        nb_ops = len(df_all)
        # Tâches terminées
        nb_fini = len(df_all[df_all["statut"] == "Fini"])
        pct_avancement = (nb_fini / nb_ops * 100) if nb_ops > 0 else 0
        
        kpi1.metric("Volume Travail Est.", f"{total_jours:.1f} j/h", help="Cumul des jours de travail estimés sur toutes les parcelles")
        kpi2.metric("Interventions", nb_ops)
        kpi3.metric("Avancement", f"{pct_avancement:.0f} %")
        kpi4.metric("Prochaine échéance", "Vendanges (simulé)") # On pourra rendre ça dynamique plus tard

        st.divider()

        # --- LIGNE 2 : GRAPHIQUES ---
        g1, g2 = st.columns(2)
        
        with g1:
            st.markdown("##### ⏳ Répartition par Cépage (Jours de travail)")
            # On groupe par cépage et on somme les jours
            df_cepage = df_all.groupby("cepage")["jours_estimes"].sum().reset_index()
            
            fig_pie = px.pie(df_cepage, values="jours_estimes", names="cepage", 
                             color="cepage", color_discrete_map=COLOR_MAP,
                             hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with g2:
            st.markdown("##### 🚦 État des tâches")
            # Compte par statut
            df_statut = df_all["statut"].value_counts().reset_index()
            df_statut.columns = ["Statut", "Nombre"]
            
            fig_bar = px.bar(df_statut, x="Statut", y="Nombre", color="Statut",
                             color_discrete_map={"Fini": "#2ecc71", "En cours": "#3498db", "A faire": "#f1c40f", "Planifié": "#95a5a6"})
            st.plotly_chart(fig_bar, use_container_width=True)

# =========================================================
# ONGLET 4 : DATA
# =========================================================
with tab_data:
    st.dataframe(pd.DataFrame(st.session_state.db_itk))
