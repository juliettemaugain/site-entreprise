import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, date, timedelta

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Pilotage & Traçabilité")
st.title("🍇 Pilotage du Vignoble - La Gauphine")

# --- 1. DONNÉES (PARCELLES) ---
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


# --- LOGIQUE DE SÉLECTION ---
selected_code_map = None
if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    for code, info in DATA_PARCELLES.items():
        if abs(info["lat"] - lat_clic) < 0.0001:
            selected_code_map = code
            break


# --- 4. ZONES D'ACTIONS (ONGLETS) ---
st.divider()

# On crée deux grands onglets : Consultation (Carte) et Planification (Calculateur)
tab_view, tab_plan, tab_data = st.tabs(["🔍 Détail Parcelle (Clic Carte)", "🚜 Planification & Calculateur", "📊 Données Brutes"])

# =========================================================
# ONGLET 1 : VUE DÉTAILLÉE (Comme avant)
# =========================================================
with tab_view:
    if selected_code_map:
        parcelle = DATA_PARCELLES[selected_code_map]
        
        st.markdown(f"### 🍇 {parcelle['nom']} <span style='font-size:0.7em; color:gray'>({parcelle['cepage']} - {parcelle['surface']} ha)</span>", unsafe_allow_html=True)

        # Données
        df_global = pd.DataFrame(st.session_state.db_itk)
        if "color_hex" not in df_global.columns: df_global["color_hex"] = "#3498db"
        else: df_global["color_hex"] = df_global["color_hex"].fillna("#3498db")
        
        df_global["start"] = pd.to_datetime(df_global["start"])
        df_global["end"] = pd.to_datetime(df_global["end"])
        
        df_filtered = df_global[df_global["parcelle_id"] == selected_code_map].copy()

        # GANTT
        if not df_filtered.empty:
            color_map_gantt = {row["tache"]: row["color_hex"] for index, row in df_filtered.iterrows()}
            
            fig = px.timeline(
                df_filtered, 
                x_start="start", x_end="end", y="tache", 
                color="tache",
                color_discrete_map=color_map_gantt,
                hover_data=["statut", "categorie", "materiel", "cadence", "jours_estimes"],
                title="Planning des interventions"
            )
            fig.update_yaxes(autorange="reversed", title="")
            st.plotly_chart(fig, use_container_width=True)
            
            # Formulaire de modification rapide (Optionnel ici si on a le planificateur)
            st.caption("ℹ️ Pour ajouter des tâches sur plusieurs parcelles, utilisez l'onglet 'Planification'.")
            
        else:
            st.info("Aucune intervention sur cette parcelle.")
    else:
        st.info("👆 Cliquez sur une parcelle de la carte pour voir son détail.")


# =========================================================
# ONGLET 2 : PLANIFICATION & CALCULATEUR (LE COEUR DE TA DEMANDE)
# =========================================================
with tab_plan:
    st.subheader("🛠️ Ajouter une intervention (Groupée)")
    
    col_gauche, col_droite = st.columns([1, 2])
    
    # --- PARTIE 1 : PARAMÈTRES DU CALCUL ---
    with col_gauche:
        st.markdown("##### 1. Paramètres de chantier")
        
        # 1. Sélection des parcelles
        # On pré-sélectionne la parcelle cliquée sur la carte si elle existe
        default_selection = [selected_code_map] if selected_code_map else []
        
        selected_parcels_ids = st.multiselect(
            "Sélectionner les parcelles concernées :",
            options=DATA_PARCELLES.keys(),
            default=default_selection,
            format_func=lambda x: f"{DATA_PARCELLES[x]['nom']} ({DATA_PARCELLES[x]['cepage']})"
        )
        
        # Calcul surface totale
        surface_totale = sum([DATA_PARCELLES[pid]['surface'] for pid in selected_parcels_ids])
        
        st.write("---")
        
        # 2. Paramètres de calcul
        cadence_input = st.number_input("Cadence (Heures / ha)", min_value=0.1, value=10.0, step=0.5, help="Temps nécessaire pour faire 1 hectare")
        nb_personnes = st.number_input("Nombre de personnes", min_value=1, value=1, step=1)
        
        # CALCUL AUTOMATIQUE
        heures_totales = surface_totale * cadence_input
        # Base : 6 heures de travail effectif par jour et par personne
        jours_estimes_calc = heures_totales / (nb_personnes * 6)
        
        # Affichage des résultats du calcul
        st.info(f"""
        **Surface Totale :** {surface_totale:.2f} ha
        **Volume Travail :** {heures_totales:.1f} heures
        
        🎯 **ESTIMATION : {jours_estimes_calc:.1f} jours**
        *(Base 6h/j/pers)*
        """)

    # --- PARTIE 2 : DÉTAILS DE LA TÂCHE ---
    with col_droite:
        st.markdown("##### 2. Détails de l'intervention")
        
        with st.form("bulk_add_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_task_name = st.text_input("Nom de l'opération", placeholder="Ex: Ebourgeonnage")
                new_cat = st.selectbox("Catégorie", ["Manuelle", "Mécanique", "Traitements", "Récolte"])
                new_color = st.color_picker("Couleur", "#2ecc71")
            
            with c2:
                new_mat = st.text_input("Matériel", placeholder="Ex: Tracteur, Sécateurs...")
                new_status = st.selectbox("Statut initial", ["Planifié", "A faire", "En cours", "Fini"])
            
            st.write("---")
            st.markdown("##### 3. Calendrier")
            
            d_col1, d_col2 = st.columns(2)
            # Date début
            start_date = d_col1.date_input("Date de début", date.today())
            
            # Suggestion de date de fin (Date début + Jours estimés)
            # On arrondit à l'entier supérieur pour la date
            jours_arrondis = int(jours_estimes_calc) if jours_estimes_calc >= 1 else 1
            suggested_end = start_date + timedelta(days=jours_arrondis)
            
            end_date = d_col2.date_input(f"Date de fin (Suggérée: {suggested_end})", value=suggested_end)
            
            submitted = st.form_submit_button("✅ Valider et Ajouter aux Plannings")
            
            if submitted:
                if not selected_parcels_ids:
                    st.error("Veuillez sélectionner au moins une parcelle !")
                else:
                    # BOUCLE D'AJOUT : On crée une tâche pour CHAQUE parcelle sélectionnée
                    timestamp_id = datetime.now().timestamp()
                    count = 0
                    
                    for pid in selected_parcels_ids:
                        new_entry = {
                            "id": f"{pid}_{timestamp_id}", # ID unique
                            "parcelle_id": pid,
                            "tache": new_task_name,
                            "categorie": new_cat,
                            "start": start_date,
                            "end": end_date,
                            "statut": new_status,
                            "cadence": cadence_input,
                            "jours_estimes": jours_estimes_calc, # On stocke le calcul
                            "materiel": new_mat,
                            "color_hex": new_color
                        }
                        st.session_state.db_itk.append(new_entry)
                        count += 1
                    
                    st.success(f"Opération '{new_task_name}' ajoutée sur {count} parcelles avec succès !")
                    # On ne met pas rerun() ici pour laisser le temps de lire le message, 
                    # mais Streamlit rechargera au prochain clic.
                    # Si tu veux forcer le refresh immédiat :
                    st.rerun()

# =========================================================
# ONGLET 3 : DATA
# =========================================================
with tab_data:
    st.dataframe(pd.DataFrame(st.session_state.db_itk))
    