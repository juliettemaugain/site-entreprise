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

# --- 1. DONNÉES RÉFÉRENTIELS (MISE EN CACHE POUR LA VITESSE) ---

@st.cache_data
def get_static_data():
    # COULEURS
    COLOR_MAP = {
        "Viognier": "blue", "Chardonnay": "orange", "Syrah": "red",
        "Grenache": "darkred", "Marselan": "purple", "Merlot": "darkblue", "Caladoc": "pink"
    }

    # PARCELLES (Tes vraies données)
    DATA_PARCELLES = {
        "VIGA03": {
            "nom": "Syrah Isabelle", "cepage": "Syrah", "surface": 0.56, "annee": 2019,
            "lat": 43.4296, "lon": 3.0925,
            "geometry": {"type": "Polygon", "coordinates": [[[3.092493, 43.429614], [3.092055, 43.428946], [3.093490, 43.428517], [3.093604, 43.428660], [3.093541, 43.428766], [3.093464, 43.428844], [3.093363, 43.428914], [3.093242, 43.428914], [3.093128, 43.428932], [3.092595, 43.429582], [3.092493, 43.429614]]]}
        },
        "VIGA_PL1": {
            "nom": "La Plaine 1 (Nord-Est)", "cepage": "Viognier", "surface": 0.50, "annee": 2015, "lat": 43.4289, "lon": 3.0930,
            "geometry": {"type": "Polygon", "coordinates": [[[3.092493, 43.429614], [3.092055, 43.428946], [3.093490, 43.428517], [3.093604, 43.428660], [3.093541, 43.428766], [3.093464, 43.428844], [3.093363, 43.428914], [3.093242, 43.428914], [3.093128, 43.428932], [3.092595, 43.429582], [3.092493, 43.429614]]]}
        },
        "VIGA_PL2": {
            "nom": "La Plaine 2 (Centre)", "cepage": "Viognier", "surface": 0.50, "annee": 2015, "lat": 43.4280, "lon": 3.0915,
            "geometry": {"type": "Polygon", "coordinates": [[[3.091501, 43.429019], [3.091162, 43.428491], [3.091705, 43.428113], [3.091867, 43.428020], [3.091113, 43.426822], [3.091776, 43.426797], [3.092495, 43.426894], [3.092798, 43.427365], [3.093003, 43.427693], [3.093447, 43.428450], [3.092072, 43.428886], [3.091501, 43.429019]]]}
        },
        "VIGA_PL3": {
            "nom": "La Plaine 3 (Est)", "cepage": "Viognier", "surface": 0.50, "annee": 2015, "lat": 43.4280, "lon": 3.0938,
            "geometry": {"type": "Polygon", "coordinates": [[[3.094155, 43.428700], [3.093952, 43.428501], [3.093641, 43.428575], [3.092930, 43.427353], [3.093673, 43.427178], [3.094435, 43.428640], [3.094155, 43.428700]]]}
        },
        "VIGA_PL4": {
            "nom": "La Plaine 4 (Ouest)", "cepage": "Viognier", "surface": 0.50, "annee": 2015, "lat": 43.4280, "lon": 3.0905,
            "geometry": {"type": "Polygon", "coordinates": [[[3.091457, 43.429064], [3.090289, 43.429451], [3.089769, 43.429290], [3.090080, 43.428529], [3.089832, 43.428031], [3.090270, 43.426915], [3.091108, 43.426837], [3.091832, 43.428013], [3.091146, 43.428492], [3.091457, 43.429064]]]}
        },
        "VIGA_PL5": {
            "nom": "La Plaine 5 (Sud-Ouest)", "cepage": "Viognier", "surface": 0.50, "annee": 2015, "lat": 43.4280, "lon": 3.0890,
            "geometry": {"type": "Polygon", "coordinates": [[[3.089321, 43.429010], [3.088299, 43.428567], [3.088895, 43.427018], [3.090190, 43.426916], [3.089321, 43.429010]]]}
        },
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

    # PRODUITS PHYTOS
    DATA_PRODUITS = {
        "Cuivre Nordox": {"unite": "kg/ha", "dose_ref": 1.25, "cible": "Mildiou", "type": "Biocontrôle", "ift": False},
        "Soufre Mouillable": {"unite": "kg/ha", "dose_ref": 12.5, "cible": "Oïdium", "type": "Biocontrôle", "ift": False},
        "Soufre Poudre": {"unite": "kg/ha", "dose_ref": 20.0, "cible": "Oïdium", "type": "Biocontrôle", "ift": False},
        "Fosétyl-Al (Sys)": {"unite": "kg/ha", "dose_ref": 2.5, "cible": "Mildiou", "type": "Chimie", "ift": True},
        "Métrafénone": {"unite": "L/ha", "dose_ref": 0.25, "cible": "Oïdium", "type": "Chimie", "ift": True},
        "Engrais Foliaire": {"unite": "L/ha", "dose_ref": 3.0, "cible": "Nutrition", "type": "Engrais", "ift": False}
    }
    
    return COLOR_MAP, DATA_PARCELLES, DATA_PRODUITS

COLOR_MAP, DATA_PARCELLES, DATA_PRODUITS = get_static_data()

# Calculs ages
annee_actuelle = datetime.now().year
for code, data in DATA_PARCELLES.items():
    data["age"] = annee_actuelle - data["annee"]
    data["color"] = COLOR_MAP.get(data["cepage"], "gray")


# --- 2. FONCTIONS LOAD/SAVE ---
def load_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df["start"] = pd.to_datetime(df["start"]).dt.date
            df["end"] = pd.to_datetime(df["end"]).dt.date
            return df.to_dict('records')
        except: return []
    else:
        # Données initiales Excel
        initial_data = []
        y_start, y_next = 2025, 2026
        tasks_template = [
            {"tache": "Nettoyage Goutte-à-goutte", "cat": "Irrigation", "start": date(y_start, 11, 10), "end": date(y_start, 12, 15), "color": "#3498db", "statut": "Fini"},
            {"tache": "Enherbement", "cat": "Mécanique", "start": date(y_start, 11, 15), "end": date(y_start, 11, 30), "color": "#2ecc71", "statut": "Fini"},
            {"tache": "Prétaille", "cat": "Mécanique", "start": date(y_start, 11, 20), "end": date(y_start, 12, 15), "color": "#f1c40f", "statut": "Fini"},
            {"tache": "Taille & Tirage", "cat": "Manuelle", "start": date(y_start, 11, 25), "end": date(y_next, 2, 28), "color": "#e74c3c", "statut": "En cours"},
            {"tache": "Epandage Compost", "cat": "Fertilisation", "start": date(y_start, 12, 1), "end": date(y_next, 1, 15), "color": "#8d6e63", "statut": "Fini"},
            {"tache": "Sécaille/Attachage", "cat": "Manuelle", "start": date(y_start, 12, 10), "end": date(y_next, 3, 15), "color": "#9b59b6", "statut": "En cours"},
            {"tache": "Suspente Goutte-à-goutte", "cat": "Irrigation", "start": date(y_next, 1, 5), "end": date(y_next, 3, 30), "color": "#3498db", "statut": "A faire"},
            {"tache": "Epandage Engrais", "cat": "Fertilisation", "start": date(y_next, 1, 25), "end": date(y_next, 2, 15), "color": "#d35400", "statut": "A faire"},
            {"tache": "Broyage du bois", "cat": "Mécanique", "start": date(y_next, 2, 1), "end": date(y_next, 3, 1), "color": "#e67e22", "statut": "A faire"},
            {"tache": "Désherbage", "cat": "Traitements", "start": date(y_next, 2, 15), "end": date(y_next, 3, 20), "color": "#27ae60", "statut": "Planifié"},
        ]
        for code in DATA_PARCELLES.keys():
            for i, t in enumerate(tasks_template):
                initial_data.append({
                    "id": f"{code}_init_{i}", "parcelle_id": code, "tache": t["tache"], "categorie": t["cat"], 
                    "start": t["start"], "end": t["end"], "statut": t["statut"], "cadence": 1.0, "jours_estimes": 0.0,
                    "materiel": "Standard", "color_hex": t["color"], "ift_value": 0.0
                })
        return initial_data

def save_data():
    if "db_itk" in st.session_state:
        pd.DataFrame(st.session_state.db_itk).to_csv(CSV_FILE, index=False)

if "db_itk" not in st.session_state:
    st.session_state.db_itk = load_data()


# --- 3. CARTE (MISE EN CACHE POUR PERFORMANCE) ---
st.subheader("🗺️ Carte du Vignoble")

@st.cache_data
def generate_map():
    # Cette fonction ne se relancera pas à chaque clic, elle est "cachée"
    avg_lat = sum([d['lat'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    avg_lon = sum([d['lon'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Esri Satellite', overlay=False, control=True).add_to(m)
    for code, info in DATA_PARCELLES.items():
        if "geometry" in info:
            folium.GeoJson(info["geometry"], style_function=lambda x, c=info.get("color","gray"): {'fillColor': c, 'color': c, 'weight': 2, 'fillOpacity': 0.4}).add_to(m)
        folium.Marker([info["lat"], info["lon"]], popup=info["nom"], icon=folium.Icon(color=info.get("color","gray"), icon="leaf", prefix="fa")).add_to(m)
    return m

# On affiche la carte cachée
m = generate_map()
col_map, col_legend = st.columns([5, 1])
with col_map:
    map_output = st_folium(m, height=450, use_container_width=True)
with col_legend:
    st.markdown("**Légende**")
    for cepage, color in COLOR_MAP.items():
        st.markdown(f"<span style='color:{color};'>■</span> {cepage}", unsafe_allow_html=True)

selected_code_map = None
if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    for code, info in DATA_PARCELLES.items():
        if abs(info["lat"] - lat_clic) < 0.0001:
            selected_code_map = code
            break


# --- 4. ONGLETS PRINCIPAUX ---
st.divider()
tab_view, tab_phyto, tab_stats, tab_data = st.tabs(["🔍 Détail Parcelle", "🧪 Traitements Phyto", "📊 Statistiques", "🗃️ Data"])

# =========================================================
# ONGLET 1 : DÉTAIL PARCELLE (Modif Standard)
# =========================================================
with tab_view:
    if selected_code_map:
        parcelle = DATA_PARCELLES[selected_code_map]
        st.markdown(f"### 🍇 {parcelle['nom']} <span style='font-size:0.7em; color:gray'>({parcelle['cepage']} - {parcelle['surface']} ha)</span>", unsafe_allow_html=True)
        
        df_global = pd.DataFrame(st.session_state.db_itk)
        for col in ["color_hex", "categorie", "materiel", "cadence", "jours_estimes", "statut", "ift_value"]:
            if col not in df_global.columns: df_global[col] = None
        df_global = df_global.fillna(value={"color_hex":"#3498db", "ift_value":0.0})
        df_global["start"] = pd.to_datetime(df_global["start"])
        df_global["end"] = pd.to_datetime(df_global["end"])
        
        df_filtered = df_global[df_global["parcelle_id"] == selected_code_map].copy()

        if not df_filtered.empty:
            color_map_gantt = {row["tache"]: row["color_hex"] for index, row in df_filtered.iterrows()}
            fig = px.timeline(
                df_filtered, x_start="start", x_end="end", y="tache", color="tache",
                color_discrete_map=color_map_gantt,
                hover_data=["statut", "categorie", "jours_estimes", "ift_value"], title="Planning"
            )
            fig.update_yaxes(autorange="reversed", title="")
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.caption("Pour modifier/supprimer une tâche standard :")
            
            # --- MODIFICATION STANDARD ---
            task_options = df_filtered[df_filtered["categorie"] != "Traitements"].to_dict('records') # On cache les phytos ici pour pas confondre
            if task_options:
                def format_func(task):
                    d = task['start'].strftime('%d/%m') if isinstance(task['start'], (datetime, pd.Timestamp)) else str(task['start'])
                    return f"{task['tache']} ({d})"

                selected_task = st.selectbox("Choisir tâche (hors phyto)", task_options, format_func=format_func)
                
                if selected_task:
                    real_index = next((i for i, item in enumerate(st.session_state.db_itk) if item["id"] == selected_task["id"]), -1)
                    
                    with st.form(key="edit_std"):
                        c1, c2 = st.columns(2)
                        with c1:
                            ns = st.selectbox("Statut", ["Planifié", "A faire", "En cours", "Fini"], index=["Planifié", "A faire", "En cours", "Fini"].index(selected_task["statut"]))
                            nc = st.color_picker("Couleur", selected_task["color_hex"])
                        with c2:
                            d1 = st.date_input("Début", selected_task["start"])
                            d2 = st.date_input("Fin", selected_task["end"])
                        del_chk = st.checkbox("Supprimer ?")
                        
                        if st.form_submit_button("Modifier"):
                            if del_chk:
                                del st.session_state.db_itk[real_index]
                                st.success("Supprimé !")
                            else:
                                st.session_state.db_itk[real_index].update({"statut": ns, "color_hex": nc, "start": d1, "end": d2})
                                st.success("À jour !")
                            save_data()
                            st.rerun()
            else:
                st.info("Aucune tâche standard modifiable.")
        else:
            st.info("Aucune intervention.")
    else:
        st.info("👆 Cliquez sur une parcelle.")


# =========================================================
# ONGLET 2 : TRAITEMENTS PHYTO (Gantt dédié + Calculateur)
# =========================================================
with tab_phyto:
    st.subheader("🧪 Traitements & Protection du Vignoble")
    
    # 1. VISUALISATION DÉDIÉE (Gantt Phyto Uniquement)
    df_all_phyto = pd.DataFrame(st.session_state.db_itk)
    if not df_all_phyto.empty and "categorie" in df_all_phyto.columns:
        df_phyto_only = df_all_phyto[df_all_phyto["categorie"] == "Traitements"].copy()
        if not df_phyto_only.empty:
            df_phyto_only["start"] = pd.to_datetime(df_phyto_only["start"])
            df_phyto_only["end"] = pd.to_datetime(df_phyto_only["end"])
            # Ajout nom parcelle
            df_phyto_only["Parcelle"] = df_phyto_only["parcelle_id"].apply(lambda x: DATA_PARCELLES.get(x, {}).get("nom", x))
            
            st.markdown("##### 📅 Calendrier des Traitements")
            fig_p = px.timeline(df_phyto_only, x_start="start", x_end="end", y="Parcelle", color="tache", title="", height=300)
            st.plotly_chart(fig_p, use_container_width=True)
        else:
            st.info("Aucun traitement enregistré.")
    
    st.divider()

    # 2. CALCULATEUR & SAISIE
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("#### 🚜 Nouvelle Application")
        with st.form("phyto_new"):
            # A. Parcelles
            sel_parc = st.multiselect("Parcelles", options=DATA_PARCELLES.keys(), format_func=lambda x: DATA_PARCELLES[x]['nom'])
            surf_tot = sum([DATA_PARCELLES[p]['surface'] for p in sel_parc])
            
            # B. Calibrage (Vitesse/Largeur)
            st.markdown("**Calibrage & Volume**")
            c_cal1, c_cal2, c_cal3 = st.columns(3)
            with c_cal1:
                vitesse = st.number_input("Vitesse (km/h)", 4.0, 10.0, 5.0)
            with c_cal2:
                largeur = st.number_input("Largeur (m)", 1.0, 3.0, 2.5) # Largeur rang ou rampe
            with c_cal3:
                vol_ha_cible = st.number_input("Objectif L/ha", 50, 500, 150)
            
            # Formule : Debit (L/min) = (L/ha * km/h * m) / 600
            debit_requis = (vol_ha_cible * vitesse * largeur) / 600
            st.info(f"💡 Pour faire **{vol_ha_cible} L/ha** à {vitesse} km/h (sur {largeur}m), il faut un débit de **{debit_requis:.2f} L/min**.")
            
            vol_cuve_total = surf_tot * vol_ha_cible
            st.markdown(f"👉 Volume Total Bouillie : **{vol_cuve_total:.0f} Litres**")
            
            # C. Produits
            st.markdown("**Produits & Doses**")
            prods = st.multiselect("Produits", options=DATA_PRODUITS.keys())
            
            details = []
            ift_tot = 0.0
            
            if prods:
                for p in prods:
                    inf = DATA_PRODUITS[p]
                    cc1, cc2 = st.columns([2, 1])
                    with cc1:
                        st.write(f"**{p}** (Ref: {inf['dose_ref']})")
                    with cc2:
                        d_u = st.number_input(f"Dose {p}", value=inf['dose_ref'], key=f"dphy_{p}")
                    
                    qte_p = d_u * surf_tot
                    st.caption(f"-> Mettre **{qte_p:.2f} {inf['unite']}** dans la cuve")
                    
                    if inf['ift'] and inf['dose_ref'] > 0:
                        ift_tot += (d_u / inf['dose_ref'])
                    details.append(f"{p}: {d_u}{inf['unite']}")

            d_app = st.date_input("Date Application", date.today())
            n_app = st.text_input("Nom Traitement", "T... Mildiou/Oïdium")

            if st.form_submit_button("✅ Enregistrer Traitement"):
                if sel_parc:
                    ts = datetime.now().timestamp()
                    str_d = " + ".join(details)
                    for pid in sel_parc:
                        st.session_state.db_itk.append({
                            "id": f"{pid}_phy_{ts}", "parcelle_id": pid, "tache": n_app,
                            "categorie": "Traitements", "start": d_app, "end": d_app,
                            "statut": "Fini", "color_hex": "#8e44ad", "ift_value": ift_tot,
                            "materiel": f"V:{vol_ha_cible}L/ha - {str_d}", "jours_estimes": 0.5
                        })
                    save_data()
                    st.success("Enregistré !")
                    st.rerun()
                else:
                    st.error("Choisir une parcelle")

    with col_right:
        st.markdown("#### ✏️ Modifier / Supprimer Phyto")
        
        # Filtre uniquement les traitements existants
        all_phyto_list = [t for t in st.session_state.db_itk if t.get("categorie") == "Traitements"]
        
        if all_phyto_list:
            # On trie par date récente
            all_phyto_list.sort(key=lambda x: x['start'], reverse=True)
            
            def fmt_p(x):
                # Récup nom parcelle pour l'affichage
                pname = DATA_PARCELLES.get(x['parcelle_id'], {}).get('nom', '?')
                return f"{x['start']} | {pname} | {x['tache']}"

            sel_edit_phy = st.selectbox("Choisir un traitement passé", all_phyto_list, format_func=fmt_p)
            
            if sel_edit_phy:
                 # Retrouver l'index
                idx_phy = next((i for i, item in enumerate(st.session_state.db_itk) if item["id"] == sel_edit_phy["id"]), -1)
                
                with st.form("edit_phyto_form"):
                    st.write(f"**{sel_edit_phy['tache']}**")
                    new_n = st.text_input("Nom", sel_edit_phy['tache'])
                    new_d = st.date_input("Date", pd.to_datetime(sel_edit_phy['start']))
                    new_ift = st.number_input("IFT", value=float(sel_edit_phy.get('ift_value', 0.0)))
                    del_phy = st.checkbox("Supprimer définitivement ?")
                    
                    if st.form_submit_button("Mettre à jour"):
                        if del_phy:
                            del st.session_state.db_itk[idx_phy]
                            st.success("Supprimé !")
                        else:
                            st.session_state.db_itk[idx_phy].update({
                                "tache": new_n, "start": new_d, "end": new_d, "ift_value": new_ift
                            })
                            st.success("Modifié !")
                        save_data()
                        st.rerun()
        else:
            st.info("Aucun historique.")


# =========================================================
# ONGLET 3 : STATISTIQUES (RESTITUÉES !)
# =========================================================
with tab_stats:
    st.subheader("📊 Tableau de Bord")
    df_all = pd.DataFrame(st.session_state.db_itk)
    
    if not df_all.empty:
        # Nettoyage
        if "jours_estimes" not in df_all.columns: df_all["jours_estimes"] = 0.0
        if "ift_value" not in df_all.columns: df_all["ift_value"] = 0.0
        df_all["jours_estimes"] = df_all["jours_estimes"].fillna(0.0)
        df_all["cepage"] = df_all["parcelle_id"].apply(lambda x: DATA_PARCELLES.get(x, {}).get("cepage", "?"))

        # 1. KPIs
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Heures Planifiées", f"{df_all['jours_estimes'].sum()*6:.0f} h")
        k2.metric("Nb Interventions", len(df_all))
        
        # Calcul IFT Moyen pondéré (approximatif pour l'exemple)
        avg_ift = df_all.groupby("parcelle_id")["ift_value"].sum().mean()
        k3.metric("IFT Moyen / Parcelle", f"{avg_ift:.2f}")
        
        nb_fini = len(df_all[df_all["statut"] == "Fini"])
        pct = (nb_fini / len(df_all) * 100) if len(df_all) > 0 else 0
        k4.metric("Avancement Global", f"{pct:.0f} %")
        
        st.divider()
        
        # 2. GRAPHIQUES
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("##### Travail par Cépage")
            grp_cep = df_all.groupby("cepage")["jours_estimes"].sum().reset_index()
            st.plotly_chart(px.pie(grp_cep, values="jours_estimes", names="cepage", color="cepage", color_discrete_map=COLOR_MAP), use_container_width=True)
        
        with g2:
            st.markdown("##### IFT par Parcelle")
            grp_ift = df_all.groupby("parcelle_id")["ift_value"].sum().reset_index()
            grp_ift["Nom"] = grp_ift["parcelle_id"].apply(lambda x: DATA_PARCELLES.get(x,{}).get("nom",x))
            st.plotly_chart(px.bar(grp_ift, x="Nom", y="ift_value", color="ift_value", color_continuous_scale="Reds"), use_container_width=True)

# ONGLET 4 : DATA
with tab_data:
    st.dataframe(pd.DataFrame(st.session_state.db_itk))