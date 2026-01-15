import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, date, timedelta
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Pilotage & Traçabilité")
st.title("🍇 Pilotage du Vignoble - La Gauphine")

CSV_FILE = "data_itk.csv"

# --- 1. DONNÉES (PARCELLES AVEC FORMES) ---
COLOR_MAP = {
    "Viognier": "blue", "Chardonnay": "orange", "Syrah": "red",
    "Grenache": "darkred", "Marselan": "purple", "Merlot": "darkblue", "Caladoc": "pink"
}

DATA_PARCELLES = {
    # --- SYRAH ISABELLE (VIGA03) ---
    "VIGA03": {
        "nom": "Syrah Isabelle", "cepage": "Syrah", "surface": 0.56, "annee": 2019,
        "lat": 43.4296, "lon": 3.0925,
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

    # --- DECOUPAGE DE LA PLAINE (1 à 5) ---
    "VIGA_PL1": {
        "nom": "La Plaine 1 (Nord-Est)", "cepage": "Viognier", "surface": 0.50, "annee": 2015, 
        "lat": 43.4289, "lon": 3.0930,
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

    # --- AUTRES PARCELLES (SIMPLES) ---
    "VIGA01": {"nom": "Vio Jeune JL", "cepage": "Viognier", "surface": 2.70, "annee": 2001, "lat": 43.4225, "lon": 3.0830},
    "VIGA04": {"nom": "Vio Plantier JL", "cepage": "Viognier", "surface": 2.54, "annee": 2014, "lat": 43.4205, "lon": 3.0850},
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


# --- 2. FONCTIONS DE CHARGEMENT ET SAUVEGARDE ---

def load_data():
    """Charge les données ou génère le planning basé sur ton EXCEL."""
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df["start"] = pd.to_datetime(df["start"]).dt.date
            df["end"] = pd.to_datetime(df["end"]).dt.date
            return df.to_dict('records')
        except: return []
    else:
        # --- GÉNÉRATION DU PLANNING TYPE (Ton Excel) ---
        initial_data = []
        y_start = 2025
        y_next = 2026
        
        for code in DATA_PARCELLES.keys():
            # Liste des tâches copiées de ton planning image
            tasks_template = [
                {"tache": "Nettoyage Goutte-à-goutte", "cat": "Irrigation", "start": date(y_start, 11, 10), "end": date(y_start, 12, 15), "color": "#3498db", "statut": "Fini"},
                {"tache": "Enherbement", "cat": "Mécanique", "start": date(y_start, 11, 15), "end": date(y_start, 11, 30), "color": "#2ecc71", "statut": "Fini"},
                {"tache": "Prétaille", "cat": "Mécanique", "start": date(y_start, 11, 20), "end": date(y_start, 12, 15), "color": "#f1c40f", "statut": "Fini"},
                {"tache": "Taille & Tirage du bois", "cat": "Manuelle", "start": date(y_start, 11, 25), "end": date(y_next, 2, 28), "color": "#e74c3c", "statut": "En cours"},
                {"tache": "Epandage Compost", "cat": "Fertilisation", "start": date(y_start, 12, 1), "end": date(y_next, 1, 15), "color": "#8d6e63", "statut": "Fini"},
                {"tache": "Entretien Palissage", "cat": "Manuelle", "start": date(y_start, 12, 10), "end": date(y_next, 3, 15), "color": "#9b59b6", "statut": "En cours"},
                {"tache": "Suspente Goutte-à-goutte", "cat": "Irrigation", "start": date(y_next, 1, 5), "end": date(y_next, 3, 30), "color": "#3498db", "statut": "A faire"},
                {"tache": "Epandage Engrais", "cat": "Fertilisation", "start": date(y_next, 1, 25), "end": date(y_next, 2, 15), "color": "#d35400", "statut": "A faire"},
                {"tache": "Broyage du bois", "cat": "Mécanique", "start": date(y_next, 2, 1), "end": date(y_next, 3, 1), "color": "#e67e22", "statut": "A faire"},
                {"tache": "Désherbage", "cat": "Traitements", "start": date(y_next, 2, 15), "end": date(y_next, 3, 20), "color": "#27ae60", "statut": "Planifié"},
            ]
            
            for i, t in enumerate(tasks_template):
                initial_data.append({
                    "id": f"{code}_init_{i}", 
                    "parcelle_id": code, 
                    "tache": t["tache"], 
                    "categorie": t["cat"], 
                    "start": t["start"], 
                    "end": t["end"],
                    "statut": t["statut"], 
                    "cadence": 1.0, 
                    "jours_estimes": 0.0,
                    "materiel": "Standard", 
                    "color_hex": t["color"]
                })
        return initial_data

def save_data():
    """Sauvegarde les données dans le fichier CSV."""
    if "db_itk" in st.session_state:
        pd.DataFrame(st.session_state.db_itk).to_csv(CSV_FILE, index=False)


# --- 3. INITIALISATION ---
if "db_itk" not in st.session_state:
    st.session_state.db_itk = load_data()


# --- 4. CARTE ---
st.subheader("🗺️ Carte du Vignoble")

col_map, col_legend = st.columns([5, 1])

with col_map:
    avg_lat = sum([d['lat'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    avg_lon = sum([d['lon'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Esri Satellite', overlay=False, control=True).add_to(m)

    for code, info in DATA_PARCELLES.items():
        if "geometry" in info:
            folium.GeoJson(
                info["geometry"],
                style_function=lambda x, color=info["color"]: {'fillColor': color, 'color': color, 'weight': 2, 'fillOpacity': 0.4},
                tooltip=f"{info['nom']} ({info['surface']} ha)"
            ).add_to(m)
        folium.Marker([info["lat"], info["lon"]], popup=f"<b>{info['nom']}</b>", icon=folium.Icon(color=info["color"], icon="leaf", prefix="fa")).add_to(m)

    map_output = st_folium(m, height=500, use_container_width=True)

with col_legend:
    st.markdown("**Légende**")
    for cepage, color in COLOR_MAP.items():
        st.markdown(f"<span style='color:{color};'>■</span> {cepage}", unsafe_allow_html=True)


# --- 5. ONGLETS ET GESTION ---
selected_code_map = None
if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    for code, info in DATA_PARCELLES.items():
        if abs(info["lat"] - lat_clic) < 0.0001:
            selected_code_map = code
            break

st.divider()
tab_view, tab_plan, tab_stats, tab_data = st.tabs(["🔍 Détail Parcelle", "🚜 Planification Groupée", "📊 Bilan & Stats", "🗃️ Données Brutes"])

# ONGLET 1 : DÉTAIL
with tab_view:
    if selected_code_map:
        parcelle = DATA_PARCELLES[selected_code_map]
        st.markdown(f"### 🍇 {parcelle['nom']} <span style='font-size:0.7em; color:gray'>({parcelle['cepage']} - {parcelle['surface']} ha)</span>", unsafe_allow_html=True)
        
        df_global = pd.DataFrame(st.session_state.db_itk)
        for col in ["color_hex", "categorie", "materiel", "cadence", "jours_estimes", "statut"]:
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
                df_filtered, x_start="start", x_end="end", y="tache", color="tache",
                color_discrete_map=color_map_gantt,
                hover_data=["statut", "categorie", "jours_estimes"], title="Planning"
            )
            fig.update_yaxes(autorange="reversed", title="")
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("🗑️ Supprimer une tâche"):
                t_del = st.selectbox("Tâche à supprimer", df_filtered["tache"].unique())
                if st.button("Confirmer suppression"):
                    st.session_state.db_itk = [i for i in st.session_state.db_itk if not (i["parcelle_id"] == selected_code_map and i["tache"] == t_del)]
                    save_data()
                    st.rerun()
        else:
            st.info("Aucune intervention.")
    else:
        st.info("👆 Cliquez sur le MARQUEUR (point) d'une parcelle pour la sélectionner.")

# ONGLET 2 : PLANIF
with tab_plan:
    st.subheader("🛠️ Ajouter une intervention")
    c_g, c_d = st.columns([1, 2])
    with c_g:
        sel_ids = st.multiselect("Parcelles", options=DATA_PARCELLES.keys(), default=[selected_code_map] if selected_code_map else [], format_func=lambda x: DATA_PARCELLES[x]['nom'])
        surf = sum([DATA_PARCELLES[p]['surface'] for p in sel_ids])
        st.caption(f"Surface: {surf:.2f} ha")
        cad = st.number_input("Cadence (h/ha)", 0.1, 100.0, 10.0)
        nb_p = st.number_input("Nb Pers", 1, 50, 1)
        j_est = (surf * cad) / (nb_p * 6)
        st.info(f"⏳ **{j_est:.1f} jours**")

    with c_d:
        with st.form("bulk"):
            c1, c2 = st.columns(2)
            with c1:
                n_t = st.text_input("Tâche", "Ebourgeonnage")
                n_c = st.selectbox("Catégorie", ["Manuelle", "Mécanique", "Traitements"])
                n_col = st.color_picker("Couleur", "#2ecc71")
            with c2:
                n_m = st.text_input("Matériel")
                n_s = st.selectbox("Statut", ["Planifié", "A faire", "En cours", "Fini"])
            d1 = st.date_input("Début", date.today())
            d2 = st.date_input("Fin", d1 + timedelta(days=int(j_est) if j_est>=1 else 1))
            
            if st.form_submit_button("✅ Valider"):
                if sel_ids:
                    ts = datetime.now().timestamp()
                    for pid in sel_ids:
                        st.session_state.db_itk.append({
                            "id": f"{pid}_{ts}", "parcelle_id": pid, "tache": n_t, "categorie": n_c,
                            "start": d1, "end": d2, "statut": n_s, "cadence": cad, "jours_estimes": j_est,
                            "materiel": n_m, "color_hex": n_col
                        })
                    save_data()
                    st.success("Ajouté !")
                    st.rerun()

# ONGLET 3 : STATS
with tab_stats:
    df_all = pd.DataFrame(st.session_state.db_itk)
    if not df_all.empty:
        if "jours_estimes" not in df_all.columns: df_all["jours_estimes"] = 0.0
        df_all["jours_estimes"] = df_all["jours_estimes"].fillna(0.0).astype(float)
        df_all["cepage"] = df_all["parcelle_id"].apply(lambda x: DATA_PARCELLES.get(x, {}).get("cepage", "?"))
        
        k1, k2, k3 = st.columns(3)
        k1.metric("Total Heures", f"{df_all['jours_estimes'].sum()*6:.0f} h") 
        k2.metric("Interventions", len(df_all))
        fini = len(df_all[df_all['statut']=='Fini'])
        k3.metric("Avancement", f"{(fini/len(df_all)*100):.0f}%")
        
        g1, g2 = st.columns(2)
        with g1: 
            st.caption("Travail par Cépage")
            st.plotly_chart(px.pie(df_all.groupby("cepage")["jours_estimes"].sum().reset_index(), values="jours_estimes", names="cepage", color="cepage", color_discrete_map=COLOR_MAP), use_container_width=True)
        with g2:
            st.caption("État des tâches")
            st.plotly_chart(px.bar(df_all["statut"].value_counts().reset_index(), x="statut", y="count", color="statut"), use_container_width=True)

# ONGLET 4 : DATA
with tab_data:
    st.dataframe(pd.DataFrame(st.session_state.db_itk))