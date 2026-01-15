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

# A. PARCELLES (Tes données géographiques)
DATA_PARCELLES = {
    # --- SYRAH ISABELLE ---
    "VIGA03": {
        "nom": "Syrah Isabelle", "cepage": "Syrah", "surface": 0.56, "annee": 2019,
        "lat": 43.4296, "lon": 3.0925,
        "geometry": {"type": "Polygon", "coordinates": [[[3.092493, 43.429614], [3.092055, 43.428946], [3.093490, 43.428517], [3.093604, 43.428660], [3.093541, 43.428766], [3.093464, 43.428844], [3.093363, 43.428914], [3.093242, 43.428914], [3.093128, 43.428932], [3.092595, 43.429582], [3.092493, 43.429614]]]}
    },
    # --- DECOUPAGE DE LA PLAINE ---
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
    # --- AUTRES ---
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

COLOR_MAP = {"Viognier": "blue", "Chardonnay": "orange", "Syrah": "red", "Grenache": "darkred", "Marselan": "purple", "Merlot": "darkblue", "Caladoc": "pink"}

# B. CATALOGUE PRODUITS PHYTOS (Exemples)
# Dose Ref = Dose Homologuée (Max légal) pour le calcul IFT
DATA_PRODUITS = {
    "Soufre Mouillable": {"unite": "kg/ha", "dose_ref": 12.5, "cible": "Oïdium", "type": "Biocontrôle", "ift": False},
    "Cuivre (Bouillie B.)": {"unite": "kg/ha", "dose_ref": 4.0, "cible": "Mildiou", "type": "Biocontrôle", "ift": False},
    "Fosétyl-Al (Sys)": {"unite": "kg/ha", "dose_ref": 2.5, "cible": "Mildiou", "type": "Conventionnel", "ift": True},
    "Métrafénone": {"unite": "L/ha", "dose_ref": 0.25, "cible": "Oïdium", "type": "Conventionnel", "ift": True},
    "Insecticide X": {"unite": "L/ha", "dose_ref": 0.5, "cible": "Cicadelle", "type": "Insecticide", "ift": True},
    "Engrais Foliaire": {"unite": "L/ha", "dose_ref": 3.0, "cible": "Nutrition", "type": "Engrais", "ift": False}
}

# --- 2. FONCTIONS GESTION DONNÉES ---

def load_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df["start"] = pd.to_datetime(df["start"]).dt.date
            df["end"] = pd.to_datetime(df["end"]).dt.date
            return df.to_dict('records')
        except: return []
    else:
        # Données par défaut (Ton Excel)
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
                    "materiel": "Standard", "color_hex": t["color"], "ift_value": 0.0 # Nouveau champ IFT
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
# AJOUT D'UN NOUVEL ONGLET SPECIFIQUE "TRAITEMENTS & IFT"
tab_view, tab_plan, tab_phyto, tab_stats, tab_data = st.tabs(["🔍 Détail Parcelle", "🚜 Planification Groupée", "🧪 Traitements & IFT", "📊 Bilan", "🗃️ Data"])

# =========================================================
# ONGLET : CALCULATEUR DE TRAITEMENTS (NOUVEAU !)
# =========================================================
with tab_phyto:
    st.subheader("🧪 Calculateur de Bouillie & Traçabilité Phyto")
    
    col_calc, col_ift = st.columns([1.5, 1])
    
    # --- PARTIE GAUCHE : LE CALCULATEUR ---
    with col_calc:
        st.markdown("#### 1. Préparation du chantier")
        with st.form("phyto_form"):
            # A. Sélection Parcelles
            sel_parcelles = st.multiselect("Parcelles à traiter", options=DATA_PARCELLES.keys(), format_func=lambda x: DATA_PARCELLES[x]['nom'])
            
            # Calcul Surface
            surf_totale = sum([DATA_PARCELLES[p]['surface'] for p in sel_parcelles])
            st.info(f"📐 Surface à traiter : **{surf_totale:.2f} ha**")
            
            c1, c2 = st.columns(2)
            with c1:
                date_traitement = st.date_input("Date", date.today())
                nom_traitement = st.text_input("Nom (ex: T2 Mildiou)", "T1 Mildiou/Oïdium")
            with c2:
                vol_cuve = st.number_input("Volume Cuve (L)", value=1000)
                vol_ha = st.number_input("Volume Bouillie / ha (L/ha)", value=150)
            
            # Calcul Volume total de bouillie nécessaire
            vol_total_bouillie = surf_totale * vol_ha
            nb_cuves = vol_total_bouillie / vol_cuve if vol_cuve > 0 else 0
            
            st.write("---")
            st.markdown("#### 2. Composition de la bouillie")
            st.caption("Sélectionnez les produits et la dose que VOUS appliquez.")
            
            # Sélection des produits (Multiselect simple pour commencer)
            prods_selected = st.multiselect("Produits", options=DATA_PRODUITS.keys())
            
            # Dictionnaire pour stocker les calculs
            details_produits = []
            ift_total_traitement = 0.0
            
            if prods_selected:
                st.markdown("**Dosage par produit :**")
                for prod in prods_selected:
                    info_p = DATA_PRODUITS[prod]
                    cp1, cp2, cp3 = st.columns([2, 1, 1])
                    
                    with cp1:
                        st.write(f"**{prod}** ({info_p['type']})")
                        st.caption(f"Cible: {info_p['cible']} | Ref: {info_p['dose_ref']} {info_p['unite']}")
                    
                    with cp2:
                        # Input dose utilisateur
                        dose_user = st.number_input(f"Dose/ha ({info_p['unite']})", value=info_p['dose_ref'], key=f"d_{prod}")
                    
                    with cp3:
                        # Calcul quantité pour la cuve
                        qte_totale = dose_user * surf_totale
                        st.metric("Total à mettre", f"{qte_totale:.1f}")
                    
                    # Calcul IFT (Si produit soumis à IFT)
                    ift_prod = 0.0
                    if info_p['ift'] and info_p['dose_ref'] > 0:
                        ift_prod = dose_user / info_p['dose_ref']
                    ift_total_traitement += ift_prod
                    
                    details_produits.append(f"{prod}: {dose_user} {info_p['unite']} (IFT {ift_prod:.2f})")

                st.write("---")
                # Résultat final pour le conducteur du tracteur
                st.success(f"""
                🚜 **POUR LE CHAUFFEUR :**
                * Volume total bouillie : **{vol_total_bouillie:.0f} Litres** ({nb_cuves:.1f} cuves de {vol_cuve}L)
                * Vitesse avancement (indicatif) : **{(vol_ha/10):.1f} L/min** (si buses standard)
                """)
                
                st.warning(f"📈 **IFT de ce traitement : {ift_total_traitement:.2f}**")

            submit_phyto = st.form_submit_button("✅ Valider et Enregistrer la Traçabilité")
            
            if submit_phyto:
                if not sel_parcelles:
                    st.error("Sélectionnez au moins une parcelle.")
                else:
                    ts = datetime.now().timestamp()
                    str_details = " | ".join(details_produits)
                    
                    for pid in sel_parcelles:
                        new_entry = {
                            "id": f"{pid}_phyto_{ts}",
                            "parcelle_id": pid,
                            "tache": nom_traitement,
                            "categorie": "Traitements", # Catégorie fixe
                            "start": date_traitement,
                            "end": date_traitement, # Dure 1 jour
                            "statut": "Fini", # On considère que c'est fait si on le rentre
                            "cadence": vol_ha, # On détourne ce champ pour stocker le Vol/ha
                            "jours_estimes": 0.5,
                            "materiel": f"Vol: {vol_total_bouillie}L - Mix: {str_details}",
                            "color_hex": "#8e44ad", # Violet pour les phytos
                            "ift_value": ift_total_traitement # On stocke l'IFT calculated
                        }
                        st.session_state.db_itk.append(new_entry)
                    
                    save_data()
                    st.success(f"Traitement enregistré sur {len(sel_parcelles)} parcelles ! IFT ajouté.")
                    st.rerun()

    # --- PARTIE DROITE : STATISTIQUES IFT ---
    with col_ift:
        st.markdown("#### 📊 Suivi IFT par Parcelle")
        
        df_all = pd.DataFrame(st.session_state.db_itk)
        if not df_all.empty and "ift_value" in df_all.columns:
            # On remplit les NaN
            df_all["ift_value"] = df_all["ift_value"].fillna(0.0)
            
            # Groupement par parcelle
            ift_per_parcelle = df_all.groupby("parcelle_id")["ift_value"].sum().reset_index()
            # Ajout des noms
            ift_per_parcelle["Nom"] = ift_per_parcelle["parcelle_id"].apply(lambda x: DATA_PARCELLES.get(x, {}).get("nom", x))
            
            # Graphique
            fig_ift = px.bar(
                ift_per_parcelle, x="Nom", y="ift_value", 
                title="IFT Cumulé (H/F/I)",
                labels={"ift_value": "IFT Total", "Nom": ""},
                color="ift_value", color_continuous_scale="Reds"
            )
            st.plotly_chart(fig_ift, use_container_width=True)
            
            # Petit tableau récap
            st.dataframe(ift_per_parcelle[["Nom", "ift_value"]].sort_values("ift_value", ascending=False), hide_index=True)
        else:
            st.info("Aucun traitement enregistré avec calcul IFT.")

# =========================================================
# LES AUTRES ONGLETS (VUE, PLANIF, STATS) RESTENT SIMILAIRES
# =========================================================

# ONGLET 1 : DÉTAIL (Similaire mais enrichi affichage IFT)
with tab_view:
    if selected_code_map:
        parcelle = DATA_PARCELLES[selected_code_map]
        st.markdown(f"### {parcelle['nom']}")
        df_global = pd.DataFrame(st.session_state.db_itk)
        # Sécurisation colonnes
        for col in ["color_hex", "categorie", "materiel", "cadence", "jours_estimes", "statut", "ift_value"]:
            if col not in df_global.columns: df_global[col] = None
        df_global = df_global.fillna(value={"color_hex":"#ccc", "ift_value":0.0})
        
        df_filtered = df_global[df_global["parcelle_id"] == selected_code_map].copy()
        df_filtered["start"] = pd.to_datetime(df_filtered["start"])
        df_filtered["end"] = pd.to_datetime(df_filtered["end"])

        if not df_filtered.empty:
            fig = px.timeline(df_filtered, x_start="start", x_end="end", y="tache", color="categorie", hover_data=["materiel", "ift_value"])
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True)
            
            # Affichage IFT Parcelle
            total_ift = df_filtered["ift_value"].sum()
            st.metric("IFT Cumulé Parcelle", f"{total_ift:.2f}")

# ONGLET 2 : PLANIFICATION (Standard)
with tab_plan:
    st.info("ℹ️ Pour les traitements phytos, utilisez l'onglet spécifique '🧪 Traitements & IFT'. Pour les autres travaux (Taille, Sol...), c'est ici.")
    # (Je garde le code précédent simplifié pour ne pas surcharger)
    c_g, c_d = st.columns([1, 2])
    with c_g:
        sel_ids = st.multiselect("Parcelles", options=DATA_PARCELLES.keys(), format_func=lambda x: DATA_PARCELLES[x]['nom'], key="plan_sel")
    with c_d:
        with st.form("bulk_std"):
            nt = st.text_input("Tâche")
            if st.form_submit_button("Ajouter"):
                ts = datetime.now().timestamp()
                for pid in sel_ids:
                    st.session_state.db_itk.append({"id": f"{pid}_{ts}", "parcelle_id": pid, "tache": nt, "categorie": "Autre", "start": date.today(), "end": date.today(), "statut": "Planifié", "color_hex": "#95a5a6", "ift_value": 0.0})
                save_data()
                st.rerun()

# ONGLET 4 : STATS
with tab_stats:
    st.write("Statistiques globales (voir onglet IFT pour le phyto).")
    df_all = pd.DataFrame(st.session_state.db_itk)
    if not df_all.empty:
        st.plotly_chart(px.pie(df_all, names="categorie", title="Répartition des travaux"), use_container_width=True)

with tab_data:
    st.dataframe(pd.DataFrame(st.session_state.db_itk))