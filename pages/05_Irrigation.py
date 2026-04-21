import streamlit as st
import folium
from streamlit_folium import st_folium
import json

# --- DONNÉES DES PARCELLES (celles que tu as partagées) ---
DATA_PARCELLES = {
    "P_00": {"nom": "Syrah Isabelle", "cepage": "Syrah", "surface": 0.56, "annee": 2019, "lat": 43.4290, "lon": 3.0930, "taille": "Palmette", "objectif": "Rosé premium", "irrigation": "Goutte à goutte", "geometry": {"type": "Polygon", "coordinates": [[[3.092493, 43.429614], [3.092055, 43.428946], [3.093490, 43.428517], [3.093604, 43.428660], [3.093541, 43.428766], [3.093464, 43.428844], [3.093363, 43.428914], [3.093242, 43.428914], [3.093128, 43.428932], [3.092595, 43.429582], [3.092493, 43.429614]]]}},
    # ... (le reste de tes données DATA_PARCELLES)
}

# --- FONCTION POUR CRÉER LA CARTE ---
def create_map():
    # Centre de la carte (coordonnées moyennes de tes parcelles)
    center_lat = sum(p["lat"] for p in DATA_PARCELLES.values()) / len(DATA_PARCELLES)
    center_lon = sum(p["lon"] for p in DATA_PARCELLES.values()) / len(DATA_PARCELLES)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14)

    # --- AJOUTER LES PARCELLES ---
    for parcelle_id, parcelle in DATA_PARCELLES.items():
        # Créer un GeoJSON pour la parcelle
        geojson = {
            "type": "Feature",
            "properties": {
                "id": parcelle_id,
                "nom": parcelle["nom"],
                "cépage": parcelle["cepage"],
                "surface": f"{parcelle['surface']} ha",
                "année": parcelle["annee"],
                "irrigation": parcelle.get("irrigation", "Non spécifié")
            },
            "geometry": parcelle["geometry"]
        }

        # Ajouter la parcelle à la carte
        folium.GeoJson(
            geojson,
            style_function=lambda x: {
                "fillColor": "#808080",  # Gris transparent
                "color": "#404040",       # Bordure gris foncé
                "weight": 1,
                "fillOpacity": 0.5
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["nom", "cépage", "surface", "année", "irrigation"],
                aliases=["Parcelle:", "Cépage:", "Surface:", "Année de plantation:", "Type d'irrigation:"],
                localize=True
            )
        ).add_to(m)

    return m

# --- AFFICHAGE DANS STREAMLIT ---
st.title("🌍 Carte des parcelles viticoles")

# Créer et afficher la carte
m = create_map()
st_folium(m, height=600, use_container_width=True)

st.success("✅ Parcelles affichées avec succès !")


# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Irrigation - Domaine Viticole", page_icon="💧")
st.title("💧 Gestion de l'Irrigation")

# --- CHEMINS DES FICHIERS ---
CSV_IRRIGATION = "data/irrigation_data.csv"
DATA_PARCELLES = st.session_state.get("DATA_PARCELLES", {})  # Récupère les données des parcelles depuis votre page existante

# --- COULEURS POUR LES ÉQUIPEMENTS ---
COLOR_EQUIPMENT = {
    "Vanne": "#3498db",      # Bleu
    "Filtre": "#e74c3c",     # Rouge
    "Pompe": "#2ecc71",      # Vert
    "Compteur": "#f39c12",   # Orange
    "Autre": "#9b59b6"       # Violet
}

STATUS_COLORS = {
    "OK": "#2ecc71",         # Vert
    "Maintenance": "#f39c12",# Orange
    "Panne": "#e74c3c"       # Rouge
}

# --- DONNÉES DES ÉQUIPEMENTS D'IRRIGATION (EXEMPLE) ---
@st.cache_data
def load_irrigation_data():
    # Si le fichier CSV existe, on le charge
    if os.path.exists(CSV_IRRIGATION):
        df = pd.read_csv(CSV_IRRIGATION)
        return df.to_dict("records")
    else:
        # Données par défaut (à remplacer par vos données réelles)
        return [
            {
                "id": "Borne A",
                "nom": "Borne A",
                "type": "Borne",
                "secteur": "DOMAINE PRINCIPAL",
                "parcelle": "P_00",  # Syrah Isabelle
                "lat": 43.4290,
                "lon": 3.0930,
                "status": "OK",
                "debit": 50.0,       # L/min
                "pression": 2.5,     # bar
                "derniere_maintenance": "2023-10-15",
                "prochaine_maintenance": "2024-04-15",
                "notes": "Vanne principale pour le secteur A"
            },
            {
                "id": "F_01",
                "nom": "Filtre Entrée Secteur B",
                "type": "Filtre",
                "secteur": "SECTEUR SAVIGNAC",
                "parcelle": "P_68",  # Viognier Haut Savignac
                "lat": 43.4175,
                "lon": 3.1167,
                "status": "Maintenance",
                "debit": 30.0,
                "pression": 1.8,
                "derniere_maintenance": "2023-11-20",
                "prochaine_maintenance": "2024-05-20",
                "notes": "Filtre à nettoyer tous les 3 mois"
            },
            # Ajoutez d'autres équipements ici...
        ]


# --- GÉNÉRATION DE LA CARTE ---
def generate_irrigation_map():
    # Créer une carte centrée sur le domaine
    m = folium.Map(location=[43.4260, 3.0900], zoom_start=14, tiles="CartoDB positron")

    # --- 1. AJOUTER LES SECTEURS (comme dans votre code existant) ---
    SECTEURS = {
        "SECTEUR GAUPHINE": [43.4025, 3.1155],
        "SECTEUR SAINTE LUCIE": [43.4405, 3.0735],
        "SECTEUR SAVIGNAC": [43.4180, 3.1230],
        "SECTEUR LA JASSE NEUVE": [43.4210, 3.0700],
        "DOMAINE PRINCIPAL": [43.4260, 3.0900]
    }

    for nom_secteur, coords in SECTEURS.items():
        folium.map.Marker(
            coords,
            icon=folium.DivIcon(
                icon_size=(300, 40),
                icon_anchor=(150, 20),
                html=f"""<div style="font-size: 18px; font-weight: 900; color: rgba(0,0,255,0.6); text-shadow: 2px 2px 10px rgba(0,0,0,0.8); text-align: center; text-transform: uppercase; letter-spacing: 3px;">{nom_secteur}</div>"""
            )
        ).add_to(m)

    # --- 2. AJOUTER LES PARCELLES (EN TRANSPARENCE) ---
    for code, info in DATA_PARCELLES.items():
        if "geometry" in info:
            folium.GeoJson(
                info["geometry"],
                style_function=lambda x: {
                    'fillColor': "#cccccc",  # Gris clair
                    'color': "#aaaaaa",     # Gris foncé
                    'weight': 1,
                    'fillOpacity': 0.2      # Très transparent
                },
                tooltip=info["nom"]
            ).add_to(m)

    # --- 3. AJOUTER LES ÉQUIPEMENTS D'IRRIGATION (SECTEUR CAZAL VIEL) ---
    # Coordonnées estimées des bornes (à ajuster avec tes données GPS réelles)
    BORNES = {
        "Borne A": {"coords": [43.4265, 3.0910], "debit": "25 m³/h", "surface": "3,5 ha"},
        "Borne B": {"coords": [43.4270, 3.0905], "debit": "20 m³/h", "surface": "2,8 ha"},
        "Borne C": {"coords": [43.4275, 3.0920], "debit": "25 m³/h", "surface": "3,5 ha"},
        "Borne D": {"coords": [43.4260, 3.0930], "debit": "35 m³/h", "surface": "4,9 ha"},
        "Borne K": {"coords": [43.4255, 3.0890], "debit": "20 m³/h", "surface": "2,8 ha"},
    }

    # Coordonnées estimées des vannes (à ajuster avec tes données GPS réelles)
    VANNES = {
        # Vannes liées à la Borne A
        "A1": {"coords": [43.4268, 3.0912], "A1": "Borne A", "parcelles": ["Roumanissas Grenache"]},
        "A2": {"coords": [43.4270, 3.0915], "A2": "Borne A", "parcelles": ["Syrah Roumanissas"]},
        "A3": {"coords": [43.4272, 3.0918], "borne": "Borne A", "parcelles": ["Roumanissas"]},
        "A4": {"coords": [43.4274, 3.0920], "borne": "Borne A", "parcelles": ["Nouveau plantier Syrah"]},
        "A5": {"coords": [43.4276, 3.0922], "borne": "Borne A", "parcelles": ["Plantier"]},
        "A6": {"coords": [43.4278, 3.0925], "borne": "Borne A", "parcelles": ["Viognier Jardin"]},
        "A7": {"coords": [43.4280, 3.0928], "borne": "Borne A", "parcelles": ["Hébram"]},

        # Vannes liées à la Borne B
        "B1": {"coords": [43.4265, 3.0900], "borne": "Borne B", "parcelles": ["Calvet"]},
        "B2": {"coords": [43.4263, 3.0895], "borne": "Borne B", "parcelles": ["La Plaine"]},
        "B3": {"coords": [43.4260, 3.0890], "borne": "Borne B", "parcelles": ["Amandier"]},
        "B4": {"coords": [43.4258, 3.0885], "borne": "Borne B", "parcelles": ["Trompet"]},

        # Vannes liées à la Borne C
        "C1": {"coords": [43.4275, 3.0925], "borne": "Borne C", "parcelles": ["Saigne"]},
        "C2": {"coords": [43.4273, 3.0922], "borne": "Borne C", "parcelles": ["Grand Bardou"]},
        "C3": {"coords": [43.4270, 3.0920], "borne": "Borne C", "parcelles": ["Terret"]},
        "C4": {"coords": [43.4268, 3.0918], "borne": "Borne C", "parcelles": ["Syrah Coural"]},
        "C5": {"coords": [43.4265, 3.0915], "borne": "Borne C", "parcelles": ["Viognier source romaine"]},
        "C6": {"coords": [43.4263, 3.0912], "borne": "Borne C", "parcelles": ["Phylloxera"]},
        "C7": {"coords": [43.4260, 3.0910], "borne": "Borne C", "parcelles": ["Viognier Alazet"]},

        # Vannes liées à la Borne D
        "D1": {"coords": [43.4255, 3.0935], "borne": "Borne D", "parcelles": ["Petit Bardou"]},
        "D2": {"coords": [43.4250, 3.0930], "borne": "Borne D", "parcelles": ["BRL - D20002"]},
        "D3": {"coords": [43.4248, 3.0925], "borne": "Borne D", "parcelles": ["BRL - D20003"]},
        "D4": {"coords": [43.4245, 3.0920], "borne": "Borne D", "parcelles": ["Da1"]},
        "D5": {"coords": [43.4243, 3.0915], "borne": "Borne D", "parcelles": ["Da2"]},
        "D6": {"coords": [43.4240, 3.0910], "borne": "Borne D", "parcelles": ["Viognier Alazet cabane"]},
        "D7": {"coords": [43.4238, 3.0905], "borne": "Borne D", "parcelles": ["Plantier terret"]},

        # Vannes liées à la Borne K
        "K1": {"coords": [43.4250, 3.0885], "borne": "Borne K", "parcelles": ["Caravane"]},
        "K2": {"coords": [43.4252, 3.0888], "borne": "Borne K", "parcelles": ["Filtre K"]},
    }

    # Ajouter les bornes à la carte
    for nom_borne, info in BORNES.items():
        folium.Marker(
            location=info["coords"],
            popup=f"""
            <b>{nom_borne}</b><br>
            Débit : {info['debit']}<br>
            Surface irriguée : {info['surface']}
            """,
            icon=folium.Icon(color="blue", icon="tint", prefix="fa")  # Icône bleue pour les bornes
        ).add_to(m)

    # Ajouter les vannes à la carte
    for nom_vanne, info in VANNES.items():
        folium.Marker(
            location=info["coords"],
            popup=f"""
            <b>Vanne {nom_vanne}</b><br>
            Borne associée : {info['borne']}<br>
            Parcelles irriguées : {', '.join(info['parcelles'])}
            """,
            icon=folium.Icon(color="green", icon="cog", prefix="fa")  # Icône verte pour les vannes
        ).add_to(m)

    return m  # N'oublie pas de retourner la carte !

# --- 4. INTERFACE UTILISATEUR ---
# Colonnes pour la carte et les filtres
col_map, col_filters = st.columns([4, 1])

with col_filters:
    st.header("Filtres")
    equipments = load_irrigation_data()

    # Filtre par type
    types = ["Tous"] + sorted(list(set([eq["type"] for eq in equipments])))
    selected_type = st.selectbox("Type d'équipement", types)

    # Filtre par statut
    statuses = ["Tous"] + sorted(list(set([eq["status"] for eq in equipments])))
    selected_status = st.selectbox("Statut", statuses)

    # Filtre par secteur
    secteurs = ["Tous"] + sorted(list(set([eq["secteur"] for eq in equipments])))
    selected_secteur = st.selectbox("Secteur", secteurs)

    # Appliquer les filtres
    filtered_equipments = [
        eq for eq in equipments
        if (selected_type == "Tous" or eq["type"] == selected_type)
        and (selected_status == "Tous" or eq["status"] == selected_status)
        and (selected_secteur == "Tous" or eq["secteur"] == selected_secteur)
    ]

    # Afficher le nombre d'équipements filtrés
    st.markdown(f"**{len(filtered_equipments)} équipements** affichés")

    # Bouton pour exporter en CSV
    if st.button("Exporter les données"):
        df = pd.DataFrame(filtered_equipments)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger CSV",
            data=csv,
            file_name="equipements_irrigation.csv",
            mime="text/csv"
        )

with col_map:
    # Générer et afficher la carte
    m = generate_irrigation_map()
    map_output = st_folium(m, height=600, use_container_width=True)

    # Afficher les détails si un équipement est cliqué
    if map_output["last_object_clicked"]:
        clicked_lat = map_output["last_object_clicked"]["lat"]
        clicked_lon = map_output["last_object_clicked"]["lng"]

        # Trouver l'équipement le plus proche
        closest_eq = None
        min_dist = float('inf')

        for eq in filtered_equipments:
            dist = ((eq["lat"] - clicked_lat)**2 + (eq["lon"] - clicked_lon)**2)**0.5
            if dist < min_dist and dist < 0.002:  # Seuil de 200m
                min_dist = dist
                closest_eq = eq

        if closest_eq:
            st.subheader(f"Détails : {closest_eq['nom']}")
            st.markdown(f"""
            - **Type** : {closest_eq['type']}
            - **Secteur** : {closest_eq['secteur']}
            - **Parcelle** : {DATA_PARCELLES.get(closest_eq['parcelle'], {}).get('nom', 'N/A')}
            - **Statut** : <span style="color: {STATUS_COLORS[closest_eq['status']]};">{closest_eq['status']}</span>
            - **Débit** : {closest_eq['debit']} L/min
            - **Pression** : {closest_eq['pression']} bar
            - **Dernière maintenance** : {closest_eq['derniere_maintenance']}
            - **Prochaine maintenance** : {closest_eq['prochaine_maintenance']}
            """, unsafe_allow_html=True)

            st.text_area("Notes", closest_eq["notes"], height=100)

            # Bouton pour signaler un problème
            if st.button("Signaler un problème", key=f"problem_{closest_eq['id']}"):
                st.warning("Fonctionnalité à implémenter : notification par email ou ticket de maintenance")

# --- LÉGENDE ---
st.sidebar.markdown("### Légende")
for eq_type, color in COLOR_EQUIPMENT.items():
    st.sidebar.markdown(f"<span style='color:{color};'>■</span> {eq_type}", unsafe_allow_html=True)

st.sidebar.markdown("---")
for status, color in STATUS_COLORS.items():
    st.sidebar.markdown(f"<span style='color:{color};'>●</span> {status}", unsafe_allow_html=True)
