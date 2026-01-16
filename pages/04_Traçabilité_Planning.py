import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, date, timedelta
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Pilotage & Traçabilité", page_icon="🍇")
st.title("🍇 Pilotage du Vignoble ")

CSV_FILE = "data_itk.csv"

# --- 1. DONNÉES RÉFÉRENTIELS ---

@st.cache_data
def get_static_data():
    # J'ai ajouté tes nouveaux cépages ici (Albarino, Cabernet Franc)
    COLOR_MAP = {
        "Viognier": "blue", 
        "Chardonnay": "orange", 
        "Syrah": "red",
        "Grenache": "#58046d",
        "Marselan": "purple", 
        "Merlot": "darkblue", 
        "Albarino": "#ffe600",      
        "Cabernet Franc": "#ed55a4", # Rouge brique
        "Autre": "gray"
    }

    DATA_PARCELLES = {
        "P_00": {
            "nom": "Syrah Isabelle", "cepage": "Syrah", "surface": 0.56, "annee": 2019,
            "lat": 43.4290, "lon": 3.0930,
            "geometry": {"type": "Polygon", "coordinates": [[[3.092493, 43.429614], [3.092055, 43.428946], [3.093490, 43.428517], [3.093604, 43.428660], [3.093541, 43.428766], [3.093464, 43.428844], [3.093363, 43.428914], [3.093242, 43.428914], [3.093128, 43.428932], [3.092595, 43.429582], [3.092493, 43.429614]]]}
        },
        "P_01": {
            "nom": "Olivette", "cepage": "Syrah", "surface": 2.57, "annee": 2010,
            "lat": 43.4278, "lon": 3.0920,
            "geometry": {"type": "Polygon", "coordinates": [[[3.091501, 43.429019], [3.091162, 43.428491], [3.091705, 43.428113], [3.091867, 43.428020], [3.091113, 43.426822], [3.091776, 43.426797], [3.092495, 43.426894], [3.092798, 43.427365], [3.093003, 43.427693], [3.093447, 43.428450], [3.092072, 43.428886], [3.091501, 43.429019]]]}
        },
        "P_02": {
            "nom": "Vio Jardin", "cepage": "Viognier", "surface": 0.86, "annee": 2015,
            "lat": 43.4280, "lon": 3.0938,
            "geometry": {"type": "Polygon", "coordinates": [[[3.094155, 43.428700], [3.093952, 43.428501], [3.093641, 43.428575], [3.092930, 43.427353], [3.093673, 43.427178], [3.094435, 43.428640], [3.094155, 43.428700]]]}
        },
        "P_03": {
            "nom": "Amandier", "cepage": "Syrah", "surface": 3.29, "annee": 2005,
            "lat": 43.4280, "lon": 3.0905,
            "geometry": {"type": "Polygon", "coordinates": [[[3.091457, 43.429064], [3.090289, 43.429451], [3.089769, 43.429290], [3.090080, 43.428529], [3.089832, 43.428031], [3.090270, 43.426915], [3.091108, 43.426837], [3.091832, 43.428013], [3.091146, 43.428492], [3.091457, 43.429064]]]}
        },
        "P_04": {
            "nom": "La Plaine", "cepage": "Viognier", "surface": 2.05, "annee": 2000, # A COMPLETER
            "lat": 43.4280, "lon": 3.0890,
            "geometry": {"type": "Polygon", "coordinates": [[[3.089321, 43.429010], [3.088299, 43.428567], [3.088895, 43.427018], [3.090190, 43.426916], [3.089321, 43.429010]]]}
        },
        "P_05": {
            "nom": "Calvet", "cepage": "Viognier", "surface": 2.03, "annee": 2000, # A COMPLETER
            "lat": 43.4275, "lon": 3.0875,
            "geometry": {"type": "Polygon", "coordinates": [[[3.088196, 43.428506], [3.086920, 43.427882], [3.086347, 43.427288], [3.087222, 43.426985], [3.088785, 43.427053], [3.088196, 43.428506]]]}
        },
        "P_06": {
            "nom": "Syrah du Virage", "cepage": "Syrah", "surface": 0.86, "annee": 2000, # A COMPLETER
            "lat": 43.4280, "lon": 3.0850,
            "geometry": {"type": "Polygon", "coordinates": [[[3.084254, 43.428442], [3.084343, 43.428253], [3.085093, 43.427973], [3.086166, 43.427432], [3.086724, 43.427942], [3.085270, 43.428434], [3.085041, 43.428234], [3.084254, 43.428442]]]}
        },
        "P_07": {
            "nom": "Roumanissas", "cepage": "Grenache", "surface": 1.90, "annee": 2000, # A COMPLETER
            "lat": 43.4315, "lon": 3.0930,
            "geometry": {"type": "Polygon", "coordinates": [[[3.092680, 43.432428], [3.092282, 43.432039], [3.091664, 43.431210], [3.093336, 43.430661], [3.093831, 43.431418], [3.093482, 43.432065], [3.092680, 43.432428]]]}
        },
        "P_08": {
            "nom": "Syrah Roumanissas", "cepage": "Syrah", "surface": 0.46, "annee": 2000,
            "lat": 43.4320, "lon": 3.0910,
            "geometry": {"type": "Polygon", "coordinates": [[[3.090032, 43.432832], [3.089855, 43.432560], [3.091954, 43.431709], [3.092126, 43.431905], [3.090506, 43.432556], [3.090032, 43.432832]]]}
        },
        "P_09": {
            "nom": "Nouveau Plantier Syrah", "cepage": "Syrah", "surface": 4.44, "annee": 2000,
            "lat": 43.4315, "lon": 3.0890,
            "geometry": {"type": "Polygon", "coordinates": [[[3.089312, 43.431234], [3.091130, 43.430625], [3.091943, 43.431654], [3.089708, 43.432425], [3.089406, 43.432350], [3.089156, 43.432134], [3.088823, 43.432119], [3.088109, 43.431714], [3.087859, 43.431237], [3.087849, 43.430950], [3.088041, 43.430651], [3.088204, 43.430287], [3.089411, 43.430613], [3.089191, 43.431156], [3.089312, 43.431234]]]}
        },
        "P_10": {
            "nom": "Syrah du Muscat", "cepage": "Syrah", "surface": 0.63, "annee": 2000,
            "lat": 43.4298, "lon": 3.0890,
            "geometry": {"type": "Polygon", "coordinates": [[[3.088852, 43.430357], [3.089367, 43.429193], [3.089635, 43.429314], [3.089829, 43.429538], [3.089472, 43.430497], [3.088852, 43.430357]]]}
        },
        "P_11": {
            "nom": "Syrah Hébram", "cepage": "Syrah", "surface": 0.61, "annee": 2000, # A COMPLETER
            "lat": 43.4296, "lon": 3.0888,
            "geometry": {"type": "Polygon", "coordinates": [[[3.088275, 43.430194], [3.088803, 43.429049], [3.089331, 43.429209], [3.088808, 43.430325], [3.088275, 43.430194]]]}
        },
        "P_12": {
            "nom": "Hébram", "cepage": "Viognier", "surface": 2.69, "annee": 2015,
            "lat": 43.4295, "lon": 3.0870,
            "geometry": {"type": "Polygon", "coordinates": [[[3.087353, 43.430411], [3.086794, 43.430547], [3.086508, 43.430276], [3.087129, 43.429710], [3.087542, 43.429046], [3.086917, 43.428733], [3.086354, 43.428368], [3.086389, 43.428112], [3.086688, 43.428010], [3.088661, 43.428963], [3.087908, 43.430773], [3.087824, 43.430769], [3.087617, 43.430450], [3.087353, 43.430411]]]}
        },
        "P_13": {
            "nom": "Caravane", "cepage": "Grenache", "surface": 1.34, "annee": 2002,
            "lat": 43.4293, "lon": 3.0855,
            "geometry": {"type": "Polygon", "coordinates": [[[3.084333, 43.429098], [3.085678, 43.428612], [3.086812, 43.429619], [3.086040, 43.429991], [3.085003, 43.429273], [3.084333, 43.429098]]]}
        },
        "P_14": {
            "nom": "Saigne", "cepage": "Syrah", "surface": 2.7, "annee": 2000,
            "lat": 43.4260, "lon": 3.0920,
            "geometry": {"type": "Polygon", "coordinates": [[[3.091024, 43.426774], [3.090444, 43.426208], [3.091976, 43.425536], [3.092239, 43.425391], [3.093237, 43.425931], [3.093889, 43.426517], [3.093726, 43.426906], [3.091813, 43.426695], [3.091024, 43.426774]]]}
        },
        "P_15": {
            "nom": "Trompet", "cepage": "Syrah", "surface": 1.81, "annee": 2000,
            "lat": 43.4265, "lon": 3.0890,
            "geometry": {"type": "Polygon", "coordinates": [[[3.090925, 43.426767], [3.088740, 43.426978], [3.087552, 43.426899], [3.087879, 43.426471], [3.088060, 43.426148], [3.090354, 43.426168], [3.090925, 43.426767]]]}
        },
        "P_16": {
            "nom": "Grand Bardou", "cepage": "Syrah", "surface": 5.9, "annee": 2000,
            "lat": 43.4245, "lon": 3.0885,
            "geometry": {"type": "Polygon", "coordinates": [[[3.088974, 43.425097], [3.088908, 43.424745], [3.086769, 43.425423], [3.086520, 43.423613], [3.089430, 43.423192], [3.090525, 43.423549], [3.090672, 43.424702], [3.090532, 43.424852], [3.089886, 43.425087], [3.088974, 43.425097]]]}
        },
        "P_17": {
            "nom": "Petit Bardou", "cepage": "Syrah", "surface": 1.95, "annee": 2000,
            "lat": 43.4245, "lon": 3.0860,
            "geometry": {"type": "Polygon", "coordinates": [[[3.086704, 43.425448], [3.085900, 43.425574], [3.085835, 43.424915], [3.085053, 43.424900], [3.085314, 43.423681], [3.086296, 43.423334], [3.086378, 43.424044], [3.086557, 43.424107], [3.086704, 43.425448]]]}
        },
        "P_18": {
            "nom": "Phylloxera", "cepage": "Albarino", "surface": 2.12, "annee": 2020,
            "lat": 43.4250, "lon": 3.0940,
            "geometry": {"type": "Polygon", "coordinates": [[[3.093742, 43.425859], [3.093026, 43.425451], [3.093087, 43.424737], [3.094175, 43.423974], [3.095034, 43.424253], [3.095071, 43.425029], [3.094447, 43.425694], [3.093742, 43.425859]]]}
        },
        "P_19": {
            "nom": "Coural", "cepage": "Viognier", "surface": 0.98, "annee": 2000,
            "lat": 43.4235, "lon": 3.0950,
            "geometry": {"type": "Polygon", "coordinates": [[[3.094200, 43.423957], [3.094706, 43.422857], [3.095547, 43.423176], [3.095547, 43.423450], [3.095083, 43.424222], [3.094200, 43.423957]]]}
        },
        "P_20": {
            "nom": "Terret", "cepage": "Grenache", "surface": 0.78, "annee": 2000,
            "lat": 43.4240, "lon": 3.0930,
            "geometry": {"type": "Polygon", "coordinates": [[[3.091950, 43.424105], [3.091740, 43.423634], [3.094020, 43.423952], [3.093483, 43.424352], [3.091950, 43.424105]]]}
        },
        "P_21": {
            "nom": "Plantier Terret", "cepage": "Syrah", "surface": 2.12, "annee": 2000,
            "lat": 43.4230, "lon": 3.0930,
            "geometry": {"type": "Polygon", "coordinates": [[[3.091425, 43.423625], [3.091598, 43.423234], [3.092167, 43.422817], [3.092148, 43.422565], [3.093180, 43.422745], [3.094268, 43.423032], [3.094397, 43.423198], [3.093990, 43.423952], [3.091425, 43.423625]]]}
        },
        "P_22": {
            "nom": "Vio Source Romaine", "cepage": "Viognier", "surface": 0.59, "annee": 2015,
            "lat": 43.4225, "lon": 3.0940,
            "geometry": {"type": "Polygon", "coordinates": [[[3.092672, 43.421963], [3.095506, 43.422745], [3.095506, 43.423029], [3.094149, 43.422610], [3.092914, 43.422219], [3.092672, 43.421963]]]}
        },
        "P_23": {
            "nom": "Syrah Coural", "cepage": "Syrah", "surface": 1.79, "annee": 2000,
            "lat": 43.4220, "lon": 3.0955,
            "geometry": {"type": "Polygon", "coordinates": [[[3.094549, 43.422348], [3.094382, 43.421606], [3.096844, 43.421228], [3.096091, 43.421929], [3.096138, 43.422321], [3.095655, 43.422685], [3.094549, 43.422348]]]}
        },
        "P_24": {
            "nom": "Albarino Coural", "cepage": "Albarino", "surface": 0.92, "annee": 2020,
            "lat": 43.4220, "lon": 3.0965,
            "geometry": {"type": "Polygon", "coordinates": [[[3.095683, 43.422806], [3.096277, 43.422267], [3.097076, 43.421187], [3.097670, 43.421417], [3.096807, 43.422523], [3.096519, 43.422469], [3.096036, 43.422921], [3.095683, 43.422806]]]}
        },
        "P_25": {
            "nom": "Vio Alazet", "cepage": "Viognier", "surface": 0.80, "annee": 2000,
            "lat": 43.4210, "lon": 3.0960,
            "geometry": {"type": "Polygon", "coordinates": [[[3.095223, 43.421390], [3.095083, 43.420776], [3.096421, 43.420614], [3.096635, 43.420506], [3.096941, 43.421140], [3.095223, 43.421390]]]}
        },
        "P_26": {
            "nom": "Vio Cabane Alazet", "cepage": "Viognier", "surface": 1.3, "annee": 2015,
            "lat": 43.4210, "lon": 3.0940,
            "geometry": {"type": "Polygon", "coordinates": [[[3.095167, 43.421363], [3.092900, 43.421680], [3.092529, 43.420627], [3.093198, 43.420992], [3.093764, 43.421073], [3.095046, 43.420776], [3.095167, 43.421363]]]}
        },
        "P_27": {
            "nom": "Merlot Alazet", "cepage": "Merlot", "surface": 0.45, "annee": 2000,
            "lat": 43.4210, "lon": 3.0922,
            "geometry": {"type": "Polygon", "coordinates": [[[3.092566, 43.421754], [3.092204, 43.420938], [3.092129, 43.420661], [3.092194, 43.420398], [3.092529, 43.420668], [3.092900, 43.421707], [3.092566, 43.421754]]]}
        },
        "P_28": {
            "nom": "Albarino Brunaude ", "cepage": "Albarino", "surface": 1.09, "annee": 2000,
            "lat": 43.4220, "lon": 3.0915,
            "geometry": {"type": "Polygon", "coordinates": [[[3.090506, 43.422866], [3.090032, 43.422326], [3.092289, 43.421334], [3.092549, 43.421955], [3.092215, 43.422009], [3.091834, 43.422029], [3.090506, 43.422866]]]}
        },
        "P_29": {
            "nom": "CF Brunaude", "cepage": "Cabernet Franc", "surface": 0.69, "annee": 2000,
            "lat": 43.4205, "lon": 3.0910,
            "geometry": {"type": "Polygon", "coordinates": [[[3.090520, 43.420806], [3.090084, 43.420165], [3.090976, 43.419834], [3.091607, 43.420412], [3.090520, 43.420806]]]}
        },
        "P_30": {
            "nom": "La Brunaude", "cepage": "Viognier", "surface": 0.83, "annee": 2015,
            "lat": 43.4218, "lon": 3.0910,
            "geometry": {"type": "Polygon", "coordinates": [[[3.090075, 43.422267], [3.089926, 43.421964], [3.092118, 43.421073], [3.092286, 43.421356], [3.090075, 43.422267]]]}
        },
        "P_31": {
            "nom": "Plantier Viognier Brunaude", "cepage": "Viognier", "surface": 0.75, "annee": 2015,
            "lat": 43.4215, "lon": 3.0910,
            "geometry": {"type": "Polygon", "coordinates": [[[3.089926, 43.421937], [3.089833, 43.421579], [3.091988, 43.420749], [3.092118, 43.421066], [3.089926, 43.421937]]]}
        }
    }

    # PRODUITS PHYTOS (INCHANGÉ)
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
    # Si le fichier CSV existe, on le lit (priorité aux données sauvegardées)
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df["start"] = pd.to_datetime(df["start"]).dt.date
            df["end"] = pd.to_datetime(df["end"]).dt.date
            return df.to_dict('records')
        except: return []
    else:
        # SINON : On génère le planning par défaut sur les NOUVELLES parcelles
        initial_data = []
        y_start, y_next = 2025, 2026
        
        # Le modèle de planning complet (selon ton Excel)
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
            # Pas de désherbage ici, on le gère dans Phyto
        ]
        
        # On applique ce modèle à CHAQUE parcelle de la nouvelle liste
        for code in DATA_PARCELLES.keys():
            for i, t in enumerate(tasks_template):
                initial_data.append({
                    "id": f"{code}_init_{i}", 
                    "parcelle_id": code, # C'est ici que le lien se fait (ex: P_00)
                    "tache": t["tache"], 
                    "categorie": t["cat"], 
                    "start": t["start"], 
                    "end": t["end"], 
                    "statut": t["statut"], 
                    "cadence": 1.0, 
                    "jours_estimes": 0.0,
                    "materiel": "Standard", 
                    "color_hex": t["color"], 
                    "ift_value": 0.0
                })
        return initial_data

def save_data():
    if "db_itk" in st.session_state:
        pd.DataFrame(st.session_state.db_itk).to_csv(CSV_FILE, index=False)

if "db_itk" not in st.session_state:
    st.session_state.db_itk = load_data()


# --- 3. CARTE (STYLE ÉPURÉ : JUSTE LE NOM) ---
st.subheader("🗺️ Carte du Vignoble")

def generate_map():
    # Centrage automatique de la carte
    avg_lat = sum([d['lat'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    avg_lon = sum([d['lon'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=16)
    
    # Fond Satellite
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri', name='Esri Satellite', overlay=False, control=True
    ).add_to(m)
    
    for code, info in DATA_PARCELLES.items():
        # 1. LA FORME (RECTANGLE/POLYGONE)
        if "geometry" in info:
            folium.GeoJson(
                info["geometry"],
                style_function=lambda x, c=info.get("color","gray"): {
                    'fillColor': c, 
                    'color': 'white',       # Contour blanc fin
                    'weight': 1, 
                    'fillOpacity': 0.5      # Transparence pour voir les rangs dessous
                },
                tooltip=f"{info['nom']} ({info['surface']} ha)"
            ).add_to(m)
        
        # 2. LE NOM (TEXTE FLOTTANT SANS CADRE)
        folium.map.Marker(
            [info["lat"], info["lon"]],
            icon=folium.DivIcon(
                icon_size=(150, 36),
                icon_anchor=(75, 18), # Centre le texte sur le point
                html=f"""
                    <div style="
                        font-size: 11px; 
                        font-weight: bold; 
                        color: white; 
                        text-shadow: 2px 2px 4px #000000; 
                        text-align: center;
                        white-space: nowrap;
                        pointer-events: none; 
                    ">
                        {info['nom']}
                    </div>
                """
            )
        ).add_to(m)
        
        # 3. ZONE DE CLIC INVISIBLE (Pour faciliter la sélection)
        # On place un cercle transparent au centre pour être sûr de capter le clic
        folium.CircleMarker(
            [info["lat"], info["lon"]],
            radius=15,
            fill_color=info.get("color","gray"),
            fill_opacity=0.0, # Invisible
            stroke=False
        ).add_to(m)

    return m

# Affichage de la carte
m = generate_map()
col_map, col_legend = st.columns([5, 1])

with col_map:
    map_output = st_folium(m, height=550, use_container_width=True)

with col_legend:
    st.markdown("**Légende**")
    for cepage, color in COLOR_MAP.items():
        st.markdown(f"<span style='color:{color};'>■</span> {cepage}", unsafe_allow_html=True)


# --- LOGIQUE DE SÉLECTION INTELLIGENTE ---
selected_code_map = None

# Si on clique sur la carte...
if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    lon_clic = map_output["last_object_clicked"]["lng"]

    # On cherche la parcelle la plus proche du point cliqué
    min_dist = 1000 # Distance arbitraire grande au début
    closest_code = None
    
    for code, info in DATA_PARCELLES.items():
        # Calcul simple de distance (Théorème de Pythagore)
        dist = ((info["lat"] - lat_clic)**2 + (info["lon"] - lon_clic)**2)**0.5
        
        # Si le clic est à moins de ~200-300 mètres du centre de la parcelle
        if dist < 0.003: 
            if dist < min_dist:
                min_dist = dist
                closest_code = code
    
    if closest_code:
        selected_code_map = closest_code

# --- 4. ONGLETS PRINCIPAUX ---
st.divider()
tab_view, tab_plan, tab_phyto, tab_stats, tab_data = st.tabs(["🔍 Détail Parcelle", "🚜 Planif Groupée", "🧪 Traitements Phyto", "📊 Statistiques", "🗃️ Data"])

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
            task_options = df_filtered[df_filtered["categorie"] != "Traitements"].to_dict('records') # On cache les phytos ici
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
# ONGLET 2 : PLANIF GROUPÉE (BIEN PRÉSENT !)
# =========================================================
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

# =========================================================
# ONGLET 3 : TRAITEMENTS PHYTO
# =========================================================
with tab_phyto:
    st.subheader("🧪 Traitements & Protection du Vignoble")
    
    # 1. VISUALISATION (GANTT AMÉLIORÉ)
    df_all_phyto = pd.DataFrame(st.session_state.db_itk)
    if not df_all_phyto.empty and "categorie" in df_all_phyto.columns:
        df_phyto_only = df_all_phyto[df_all_phyto["categorie"] == "Traitements"].copy()
        if not df_phyto_only.empty:
            df_phyto_only["start"] = pd.to_datetime(df_phyto_only["start"])
            df_phyto_only["end"] = pd.to_datetime(df_phyto_only["end"])
            df_phyto_only["Parcelle"] = df_phyto_only["parcelle_id"].apply(lambda x: DATA_PARCELLES.get(x, {}).get("nom", x))
            
            st.markdown("##### 📅 Calendrier des Traitements")
            fig_p = px.timeline(
                df_phyto_only, x_start="start", x_end="end", y="Parcelle", 
                color="tache", text="tache", title="",
                height=350 + (len(df_phyto_only["Parcelle"].unique()) * 20)
            )
            # Autoscale et format date
            fig_p.update_layout(
                xaxis=dict(title="Date", tickformat="%d/%m", range=[date(date.today().year, 1, 1), date(date.today().year, 12, 31)]),
                yaxis=dict(title=""), showlegend=True
            )
            fig_p.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_p, use_container_width=True)
        else:
            st.info("Aucun traitement enregistré.")
    
    st.divider()

    # 2. CALCULATEUR
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("#### 🚜 Nouvelle Application")
        with st.form("phyto_new"):
            # A. Parcelles
            sel_parc = st.multiselect("Parcelles", options=DATA_PARCELLES.keys(), format_func=lambda x: DATA_PARCELLES[x]['nom'])
            surf_tot = sum([DATA_PARCELLES[p]['surface'] for p in sel_parc])
            
            # B. Calibrage
            st.markdown("**Calibrage**")
            c1, c2, c3 = st.columns(3)
            with c1:
                vitesse = st.number_input("Vitesse (km/h)", 4.0, 10.0, 5.0)
            with c2:
                largeur = st.number_input("Largeur (m)", 1.0, 3.0, 2.5)
            with c3:
                vol_ha_cible = st.number_input("Objectif L/ha", 50, 500, 150)
            
            debit_requis = (vol_ha_cible * vitesse * largeur) / 600
            st.info(f"💡 Débit requis : **{debit_requis:.2f} L/min** (pour {vol_ha_cible} L/ha)")
            
            vol_cuve_total = surf_tot * vol_ha_cible
            st.markdown(f"👉 Volume Total Bouillie : **{vol_cuve_total:.0f} Litres**")
            
            # C. Produits
            st.markdown("**Produits**")
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
                    st.caption(f"-> Mettre **{qte_p:.2f} {inf['unite']}**")
                    
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
        all_phyto_list = [t for t in st.session_state.db_itk if t.get("categorie") == "Traitements"]
        
        if all_phyto_list:
            all_phyto_list.sort(key=lambda x: x['start'], reverse=True)
            def fmt_p(x):
                pname = DATA_PARCELLES.get(x['parcelle_id'], {}).get('nom', '?')
                return f"{x['start']} | {pname} | {x['tache']}"

            sel_edit_phy = st.selectbox("Choisir un traitement passé", all_phyto_list, format_func=fmt_p)
            
            if sel_edit_phy:
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
                            st.session_state.db_itk[idx_phy].update({"tache": new_n, "start": new_d, "end": new_d, "ift_value": new_ift})
                            st.success("Modifié !")
                        save_data()
                        st.rerun()
        else:
            st.info("Aucun historique.")


# =========================================================
# ONGLET 4 : STATISTIQUES (RESTITUÉES !)
# =========================================================
with tab_stats:
    st.subheader("📊 Tableau de Bord")
    df_all = pd.DataFrame(st.session_state.db_itk)
    
    if not df_all.empty:
        if "jours_estimes" not in df_all.columns: df_all["jours_estimes"] = 0.0
        if "ift_value" not in df_all.columns: df_all["ift_value"] = 0.0
        df_all["jours_estimes"] = df_all["jours_estimes"].fillna(0.0)
        df_all["cepage"] = df_all["parcelle_id"].apply(lambda x: DATA_PARCELLES.get(x, {}).get("cepage", "?"))

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Heures Planifiées", f"{df_all['jours_estimes'].sum()*6:.0f} h")
        k2.metric("Nb Interventions", len(df_all))
        avg_ift = df_all.groupby("parcelle_id")["ift_value"].sum().mean()
        k3.metric("IFT Moyen / Parcelle", f"{avg_ift:.2f}")
        nb_fini = len(df_all[df_all["statut"] == "Fini"])
        pct = (nb_fini / len(df_all) * 100) if len(df_all) > 0 else 0
        k4.metric("Avancement Global", f"{pct:.0f} %")
        
        st.divider()
        
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

# ONGLET 5 : DATA
with tab_data:
    st.dataframe(pd.DataFrame(st.session_state.db_itk))