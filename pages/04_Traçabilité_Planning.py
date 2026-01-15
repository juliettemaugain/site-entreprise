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

# --- 1. DONNÉES RÉFÉRENTIELS ---

COLOR_MAP = {
    "Viognier": "blue", "Chardonnay": "orange", "Syrah": "red",
    "Grenache": "darkred", "Marselan": "purple", "Merlot": "darkblue", "Caladoc": "pink"
}

# TES PARCELLES (Complètes)
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

# Calculs automatiques
annee_actuelle = datetime.now().year
for code, data in DATA_PARCELLES.items():
    data["age"] = annee_actuelle - data["annee"]
    data["color"] = COLOR_MAP.get(data["cepage"], "gray")


# --- MISE A JOUR : BASE PRODUITS AVEC TES DOSES ---
DATA_PRODUITS = {
    "Cuivre Nordox": {
        "unite": "kg/ha", 
        "dose_ref": 1.25, # TA dose de référence
        "cible": "Mildiou", 
        "type": "Biocontrôle", 
        "ift": False
    },
    "Soufre Mouillable": {
        "unite": "kg/ha", 
        "dose_ref": 12.5, 
        "cible": "Oïdium", 
        "type": "Biocontrôle", 
        "ift": False
    },
    "Soufre Poudre": {
        "unite": "kg/ha", 
        "dose_ref": 20.0, 
        "cible": "Oïdium", 
        "type": "Biocontrôle", 
        "ift": False
    },
    "Fosétyl-Al (Sys)": {
        "unite": "kg/ha", 
        "dose_ref": 2.5, 
        "cible": "Mildiou", 
        "type": "Chimie", 
        "ift": True
    },
    "Métrafénone": {
        "unite": "L/ha", 
        "dose_ref": 0.25, 
        "cible": "Oïdium", 
        "type": "Chimie", 
        "ift": True
    },
    "Engrais Foliaire": {
        "unite": "L/ha", 
        "dose_ref": 3.0, 
        "cible": "Nutrition", 
        "type": "Engrais", 
        "ift": False
    }
}


# --- 2. FONCTIONS DE CHARGEMENT ET SAUVEGARDE ---
def load_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df["start"] = pd.to_datetime(df["start"]).dt.date
            df["end"] = pd.to_datetime(df["end"]).dt.date
            return df.to_dict('records')
        except: return []
    else:
        # Données par défaut (Ton Excel complet)
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


# --- 3. CARTE ---
st.subheader("🗺️ Carte du Vignoble")
col_map, col_legend = st.columns([5, 1])
with col_map:
    avg_lat = sum([d['lat'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    avg_lon = sum([d['lon'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Esri Satellite', overlay=False, control=True).add_to(m)
    for code, info in DATA_PARCELLES.items():
        if "geometry" in info:
            folium.GeoJson(info["geometry"], style_function=lambda x, color=DATA_PARCELLES[code].get("color", "gray"): {'fillColor': color, 'color': color, 'weight': 2, 'fillOpacity': 0.4}).add_to(m)
        folium.Marker([info["lat"], info["lon"]], popup=info["nom"], icon=folium.Icon(color=DATA_PARCELLES[code].get("color", "gray"), icon="leaf", prefix="fa")).add_to(m)
    map_output = st_folium(m, height=450, use_container_width=True)

selected_code_map = None
if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    for code, info in DATA_PARCELLES.items():
        if abs(info["lat"] - lat_clic) < 0.0001:
            selected_code_map = code
            break

# --- 4. ONGLETS DE GESTION ---
st.divider()
tab_view, tab_plan, tab_phyto, tab_stats, tab_data = st.tabs(["🔍 Détail & Modif", "🚜 Planif Groupée", "🧪 Traitements Phyto", "📊 Stats", "🗃️ Data"])

# ONGLET 1 : DÉTAIL & MODIFICATION
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
            st.subheader("✏️ Modifier une intervention")
            task_options = df_filtered.to_dict('records')
            
            def format_func(task):
                d = task['start'].strftime('%d/%m') if isinstance(task['start'], (datetime, pd.Timestamp)) else str(task['start'])
                return f"{task['tache']} ({d}) - {task['statut']}"

            selected_task = st.selectbox("Choisir la tâche :", task_options, format_func=format_func)
            
            if selected_task:
                real_index = -1
                for idx, item in enumerate(st.session_state.db_itk):
                    if item["id"] == selected_task["id"]:
                        real_index = idx
                        break
                
                with st.form(key="edit_task_form"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        new_statut = st.selectbox("Statut", ["Planifié", "A faire", "En cours", "Fini"], index=["Planifié", "A faire", "En cours", "Fini"].index(selected_task["statut"]))
                        new_color = st.color_picker("Couleur", selected_task["color_hex"])
                    with c2:
                        d_s = selected_task["start"] if isinstance(selected_task["start"], date) else selected_task["start"].date()
                        d_e = selected_task["end"] if isinstance(selected_task["end"], date) else selected_task["end"].date()
                        new_start = st.date_input("Début", d_s)
                        new_end = st.date_input("Fin", d_e)
                    with c3:
                        new_mat = st.text_input("Matériel / Mélange", value=str(selected_task["materiel"]))
                        del_chk = st.checkbox("Supprimer ?")

                    if st.form_submit_button("Enregistrer"):
                        if del_chk:
                            del st.session_state.db_itk[real_index]
                            st.success("Supprimé !")
                        else:
                            st.session_state.db_itk[real_index].update({
                                "statut": new_statut, "color_hex": new_color,
                                "start": new_start, "end": new_end, "materiel": new_mat
                            })
                            st.success("Modifié !")
                        save_data()
                        st.rerun()
        else:
            st.info("Rien ici.")
    else:
        st.info("👆 Cliquez sur une parcelle.")

# ONGLET 2 : PLANIF GROUPÉE
with tab_plan:
    st.subheader("🛠️ Ajouter une intervention (Sauf Phyto)")
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
            
            if st.form_submit_button("Valider"):
                if sel_ids:
                    ts = datetime.now().timestamp()
                    for pid in sel_ids:
                        st.session_state.db_itk.append({
                            "id": f"{pid}_{ts}", "parcelle_id": pid, "tache": n_t, "categorie": n_c,
                            "start": d1, "end": d2, "statut": n_s, "cadence": cad, "jours_estimes": j_est,
                            "materiel": n_m, "color_hex": n_col, "ift_value": 0.0
                        })
                    save_data()
                    st.success("Ajouté !")
                    st.rerun()

# --- NOUVEL ONGLET PHYTO (AJUSTÉ SELON TA DEMANDE) ---
with tab_phyto:
    st.subheader("🧪 Calculateur Phyto & IFT")
    
    col_calc, col_ift = st.columns([1.5, 1])
    
    with col_calc:
        st.markdown("**1. Préparation**")
        with st.form("phyto_form"):
            # Selection parcelles
            sel_parc = st.multiselect("Parcelles à traiter", options=DATA_PARCELLES.keys(), format_func=lambda x: DATA_PARCELLES[x]['nom'])
            surf_tot = sum([DATA_PARCELLES[p]['surface'] for p in sel_parc])
            st.info(f"Surface Totale : **{surf_tot:.2f} ha**")
            
            c1, c2 = st.columns(2)
            with c1:
                d_trait = st.date_input("Date du traitement", date.today())
                n_trait = st.text_input("Nom", "T2 Mildiou/Oïdium")
            with c2:
                st.caption("Volume de Bouillie")
                vol_ha = st.number_input("L/ha (Bouillie)", value=150)
                vol_cuve = st.number_input("Volume Cuve (L)", value=1000)
            
            vol_tot = surf_tot * vol_ha
            nb_cuves = vol_tot / vol_cuve
            st.markdown(f"👉 Besoin total : **{vol_tot:.0f} L** ({nb_cuves:.1f} cuves)")
            
            st.write("---")
            st.markdown("**2. Composition (Produit par produit)**")
            
            # Sélection Multi-produits
            prods = st.multiselect("Choisir les produits", options=DATA_PRODUITS.keys())
            
            details = []
            ift_tot = 0.0
            
            if prods:
                st.markdown("##### 🧪 Dosage dans la cuve")
                for p in prods:
                    inf = DATA_PRODUITS[p]
                    
                    # On affiche la dose de référence pré-remplie
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    with col_a:
                        st.write(f"**{p}**")
                        st.caption(f"Ref: {inf['dose_ref']} {inf['unite']}")
                    
                    with col_b:
                        # Ici l'utilisateur peut changer la dose s'il module
                        d_user = st.number_input(f"Dose ({inf['unite']})", value=inf['dose_ref'], key=f"d_{p}")
                    
                    with col_c:
                        # Calcul quantité TOTALE pour la surface choisie
                        qte_totale = d_user * surf_tot
                        st.metric("Total à mettre", f"{qte_totale:.2f}")

                    # Calcul IFT produit
                    ift_p = 0.0
                    if inf['ift'] and inf['dose_ref'] > 0:
                        ift_p = d_user / inf['dose_ref']
                    
                    ift_tot += ift_p
                    details.append(f"{p}: {d_user} {inf['unite']}")

                st.warning(f"📈 IFT Total de ce passage : {ift_tot:.2f}")

            if st.form_submit_button("✅ Enregistrer Traitement"):
                if sel_parc:
                    ts = datetime.now().timestamp()
                    str_det = " + ".join(details)
                    for pid in sel_parc:
                        st.session_state.db_itk.append({
                            "id": f"{pid}_phyto_{ts}", 
                            "parcelle_id": pid, 
                            "tache": n_trait,
                            "categorie": "Traitements", 
                            "start": d_trait, 
                            "end": d_trait,
                            "statut": "Fini", 
                            "color_hex": "#8e44ad", 
                            "ift_value": ift_tot,
                            "materiel": f"{str_det} (Vol:{vol_ha}L/ha)", 
                            "jours_estimes": 0.5
                        })
                    save_data()
                    st.success("Enregistré !")
                    st.rerun()

    with col_ift:
        st.markdown("**Suivi IFT par Parcelle**")
        df_all = pd.DataFrame(st.session_state.db_itk)
        if not df_all.empty and "ift_value" in df_all.columns:
            df_all["ift_value"] = df_all["ift_value"].fillna(0.0)
            res = df_all.groupby("parcelle_id")["ift_value"].sum().reset_index()
            res["Nom"] = res["parcelle_id"].apply(lambda x: DATA_PARCELLES.get(x, {}).get("nom", x))
            st.dataframe(res[["Nom", "ift_value"]], hide_index=True)
            st.plotly_chart(px.bar(res, x="Nom", y="ift_value", color="ift_value"), use_container_width=True)

# ONGLET 4 : STATS
with tab_stats:
    df_all = pd.DataFrame(st.session_state.db_itk)
    if not df_all.empty:
        if "jours_estimes" not in df_all.columns: df_all["jours_estimes"] = 0.0
        st.metric("Total Heures", f"{df_all['jours_estimes'].sum()*6:.0f} h")
        st.plotly_chart(px.pie(df_all, names="categorie"), use_container_width=True)

# ONGLET 5 : DATA
with tab_data:
    st.dataframe(pd.DataFrame(st.session_state.db_itk))