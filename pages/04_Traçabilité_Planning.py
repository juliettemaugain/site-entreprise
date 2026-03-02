import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, date, timedelta
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Pilotage & Traçabilité", page_icon="🍇")
st.title("🍇 Pilotage du Vignoble")

CSV_FILE = "data_itk.csv"


# --- 1. DONNÉES RÉFÉRENTIELS ---

@st.cache_data
def get_static_data():
    COLOR_MAP = {
        "Viognier": "blue", 
        "Chardonnay": "orange", 
        "Syrah": "red",
        "Grenache": "#aaff00",
        "Marselan": "purple", 
        "Merlot": "darkblue", 
        "Albarino": "#ffe600",      
        "Cabernet Franc": "#ff9900",
        "Cinsault":"#ed55a4",
        "Autre": "gray"
    }

    DATA_PARCELLES = {
        "P_00": {"nom": "Syrah Isabelle", "cepage": "Syrah", "surface": 0.56, "annee": 2019, "lat": 43.4290, "lon": 3.0930, "geometry": {"type": "Polygon", "coordinates": [[[3.092493, 43.429614], [3.092055, 43.428946], [3.093490, 43.428517], [3.093604, 43.428660], [3.093541, 43.428766], [3.093464, 43.428844], [3.093363, 43.428914], [3.093242, 43.428914], [3.093128, 43.428932], [3.092595, 43.429582], [3.092493, 43.429614]]]}},
        "P_01": {"nom": "Olivette", "cepage": "Syrah", "surface": 2.57, "annee": 2010, "lat": 43.4278, "lon": 3.0920, "geometry": {"type": "Polygon", "coordinates": [[[3.091501, 43.429019], [3.091162, 43.428491], [3.091705, 43.428113], [3.091867, 43.428020], [3.091113, 43.426822], [3.091776, 43.426797], [3.092495, 43.426894], [3.092798, 43.427365], [3.093003, 43.427693], [3.093447, 43.428450], [3.092072, 43.428886], [3.091501, 43.429019]]]}},
        "P_02": {"nom": "Vio Jardin", "cepage": "Viognier", "surface": 0.86, "annee": 2015, "lat": 43.4280, "lon": 3.0938, "geometry": {"type": "Polygon", "coordinates": [[[3.094155, 43.428700], [3.093952, 43.428501], [3.093641, 43.428575], [3.092930, 43.427353], [3.093673, 43.427178], [3.094435, 43.428640], [3.094155, 43.428700]]]}},
        "P_03": {"nom": "Amandier", "cepage": "Syrah", "surface": 3.29, "annee": 2005, "lat": 43.4280, "lon": 3.0905, "geometry": {"type": "Polygon", "coordinates": [[[3.091457, 43.429064], [3.090289, 43.429451], [3.089769, 43.429290], [3.090080, 43.428529], [3.089832, 43.428031], [3.090270, 43.426915], [3.091108, 43.426837], [3.091832, 43.428013], [3.091146, 43.428492], [3.091457, 43.429064]]]}},
        "P_04": {"nom": "La Plaine", "cepage": "Viognier", "surface": 2.05, "annee": 2000, "lat": 43.4280, "lon": 3.0890, "geometry": {"type": "Polygon", "coordinates": [[[3.089321, 43.429010], [3.088299, 43.428567], [3.088895, 43.427018], [3.090190, 43.426916], [3.089321, 43.429010]]]}},
        "P_05": {"nom": "Calvet", "cepage": "Viognier", "surface": 2.03, "annee": 2000, "lat": 43.4275, "lon": 3.0875, "geometry": {"type": "Polygon", "coordinates": [[[3.088196, 43.428506], [3.086920, 43.427882], [3.086347, 43.427288], [3.087222, 43.426985], [3.088785, 43.427053], [3.088196, 43.428506]]]}},
        "P_06": {"nom": "Syrah du Virage", "cepage": "Syrah", "surface": 0.86, "annee": 2000, "lat": 43.4280, "lon": 3.0850, "geometry": {"type": "Polygon", "coordinates": [[[3.084254, 43.428442], [3.084343, 43.428253], [3.085093, 43.427973], [3.086166, 43.427432], [3.086724, 43.427942], [3.085270, 43.428434], [3.085041, 43.428234], [3.084254, 43.428442]]]}},
        "P_07": {"nom": "Roumanissas", "cepage": "Grenache", "surface": 1.90, "annee": 2000, "lat": 43.4315, "lon": 3.0930, "geometry": {"type": "Polygon", "coordinates": [[[3.092680, 43.432428], [3.092282, 43.432039], [3.091664, 43.431210], [3.093336, 43.430661], [3.093831, 43.431418], [3.093482, 43.432065], [3.092680, 43.432428]]]}},
        "P_08": {"nom": "Syrah Roumanissas", "cepage": "Syrah", "surface": 0.46, "annee": 2000, "lat": 43.4320, "lon": 3.0910, "geometry": {"type": "Polygon", "coordinates": [[[3.090032, 43.432832], [3.089855, 43.432560], [3.091954, 43.431709], [3.092126, 43.431905], [3.090506, 43.432556], [3.090032, 43.432832]]]}},
        "P_09": {"nom": "Nouveau Plantier Syrah", "cepage": "Syrah", "surface": 4.44, "annee": 2000, "lat": 43.4315, "lon": 3.0890, "geometry": {"type": "Polygon", "coordinates": [[[3.089312, 43.431234], [3.091130, 43.430625], [3.091943, 43.431654], [3.089708, 43.432425], [3.089406, 43.432350], [3.089156, 43.432134], [3.088823, 43.432119], [3.088109, 43.431714], [3.087859, 43.431237], [3.087849, 43.430950], [3.088041, 43.430651], [3.088204, 43.430287], [3.089411, 43.430613], [3.089191, 43.431156], [3.089312, 43.431234]]]}},
        "P_10": {"nom": "Syrah du Muscat", "cepage": "Syrah", "surface": 0.63, "annee": 2000, "lat": 43.4298, "lon": 3.0890, "geometry": {"type": "Polygon", "coordinates": [[[3.088852, 43.430357], [3.089367, 43.429193], [3.089635, 43.429314], [3.089829, 43.429538], [3.089472, 43.430497], [3.088852, 43.430357]]]}},
        "P_11": {"nom": "Syrah Hébram", "cepage": "Syrah", "surface": 0.61, "annee": 2000, "lat": 43.4296, "lon": 3.0888, "geometry": {"type": "Polygon", "coordinates": [[[3.088275, 43.430194], [3.088803, 43.429049], [3.089331, 43.429209], [3.088808, 43.430325], [3.088275, 43.430194]]]}},
        "P_12": {"nom": "Hébram", "cepage": "Viognier", "surface": 2.69, "annee": 2015, "lat": 43.4295, "lon": 3.0870, "geometry": {"type": "Polygon", "coordinates": [[[3.087353, 43.430411], [3.086794, 43.430547], [3.086508, 43.430276], [3.087129, 43.429710], [3.087542, 43.429046], [3.086917, 43.428733], [3.086354, 43.428368], [3.086389, 43.428112], [3.086688, 43.428010], [3.088661, 43.428963], [3.087908, 43.430773], [3.087824, 43.430769], [3.087617, 43.430450], [3.087353, 43.430411]]]}},
        "P_13": {"nom": "Caravane", "cepage": "Grenache", "surface": 1.34, "annee": 2002, "lat": 43.4293, "lon": 3.0855, "geometry": {"type": "Polygon", "coordinates": [[[3.084333, 43.429098], [3.085678, 43.428612], [3.086812, 43.429619], [3.086040, 43.429991], [3.085003, 43.429273], [3.084333, 43.429098]]]}},
        "P_14": {"nom": "Saigne", "cepage": "Syrah", "surface": 2.7, "annee": 2000, "lat": 43.4260, "lon": 3.0920, "geometry": {"type": "Polygon", "coordinates": [[[3.091024, 43.426774], [3.090444, 43.426208], [3.091976, 43.425536], [3.092239, 43.425391], [3.093237, 43.425931], [3.093889, 43.426517], [3.093726, 43.426906], [3.091813, 43.426695], [3.091024, 43.426774]]]}},
        "P_15": {"nom": "Trompet", "cepage": "Syrah", "surface": 1.81, "annee": 2000, "lat": 43.4265, "lon": 3.0890, "geometry": {"type": "Polygon", "coordinates": [[[3.090925, 43.426767], [3.088740, 43.426978], [3.087552, 43.426899], [3.087879, 43.426471], [3.088060, 43.426148], [3.090354, 43.426168], [3.090925, 43.426767]]]}},
        "P_16": {"nom": "Grand Bardou", "cepage": "Syrah", "surface": 5.9, "annee": 2000, "lat": 43.4245, "lon": 3.0885, "geometry": {"type": "Polygon", "coordinates": [[[3.088974, 43.425097], [3.088908, 43.424745], [3.086769, 43.425423], [3.086520, 43.423613], [3.089430, 43.423192], [3.090525, 43.423549], [3.090672, 43.424702], [3.090532, 43.424852], [3.089886, 43.425087], [3.088974, 43.425097]]]}},
        "P_17": {"nom": "Petit Bardou", "cepage": "Syrah", "surface": 1.95, "annee": 2000, "lat": 43.4245, "lon": 3.0860, "geometry": {"type": "Polygon", "coordinates": [[[3.086704, 43.425448], [3.085900, 43.425574], [3.085835, 43.424915], [3.085053, 43.424900], [3.085314, 43.423681], [3.086296, 43.423334], [3.086378, 43.424044], [3.086557, 43.424107], [3.086704, 43.425448]]]}},
        "P_18": {"nom": "Phylloxera", "cepage": "Albarino", "surface": 2.12, "annee": 2020, "lat": 43.4250, "lon": 3.0940, "geometry": {"type": "Polygon", "coordinates": [[[3.093742, 43.425859], [3.093026, 43.425451], [3.093087, 43.424737], [3.094175, 43.423974], [3.095034, 43.424253], [3.095071, 43.425029], [3.094447, 43.425694], [3.093742, 43.425859]]]}},
        "P_19": {"nom": "Coural", "cepage": "Viognier", "surface": 0.98, "annee": 2000, "lat": 43.4235, "lon": 3.0950, "geometry": {"type": "Polygon", "coordinates": [[[3.094200, 43.423957], [3.094706, 43.422857], [3.095547, 43.423176], [3.095547, 43.423450], [3.095083, 43.424222], [3.094200, 43.423957]]]}},
        "P_20": {"nom": "Terret", "cepage": "Grenache", "surface": 0.78, "annee": 2000, "lat": 43.4240, "lon": 3.0930, "geometry": {"type": "Polygon", "coordinates": [[[3.091950, 43.424105], [3.091740, 43.423634], [3.094020, 43.423952], [3.093483, 43.424352], [3.091950, 43.424105]]]}},
        "P_21": {"nom": "Plantier Terret", "cepage": "Syrah", "surface": 2.12, "annee": 2000, "lat": 43.4230, "lon": 3.0930, "geometry": {"type": "Polygon", "coordinates": [[[3.091425, 43.423625], [3.091598, 43.423234], [3.092167, 43.422817], [3.092148, 43.422565], [3.093180, 43.422745], [3.094268, 43.423032], [3.094397, 43.423198], [3.093990, 43.423952], [3.091425, 43.423625]]]}},
        "P_22": {"nom": "Vio Source Romaine", "cepage": "Viognier", "surface": 0.59, "annee": 2015, "lat": 43.4225, "lon": 3.0940, "geometry": {"type": "Polygon", "coordinates": [[[3.092672, 43.421963], [3.095506, 43.422745], [3.095506, 43.423029], [3.094149, 43.422610], [3.092914, 43.422219], [3.092672, 43.421963]]]}},
        "P_23": {"nom": "Syrah Coural", "cepage": "Syrah", "surface": 1.79, "annee": 2000, "lat": 43.4220, "lon": 3.0955, "geometry": {"type": "Polygon", "coordinates": [[[3.094549, 43.422348], [3.094382, 43.421606], [3.096844, 43.421228], [3.096091, 43.421929], [3.096138, 43.422321], [3.095655, 43.422685], [3.094549, 43.422348]]]}},
        "P_24": {"nom": "Albarino Coural", "cepage": "Albarino", "surface": 0.92, "annee": 2020, "lat": 43.4220, "lon": 3.0965, "geometry": {"type": "Polygon", "coordinates": [[[3.095683, 43.422806], [3.096277, 43.422267], [3.097076, 43.421187], [3.097670, 43.421417], [3.096807, 43.422523], [3.096519, 43.422469], [3.096036, 43.422921], [3.095683, 43.422806]]]}},
        "P_25": {"nom": "Vio Alazet", "cepage": "Viognier", "surface": 0.80, "annee": 2000, "lat": 43.4210, "lon": 3.0960, "geometry": {"type": "Polygon", "coordinates": [[[3.095223, 43.421390], [3.095083, 43.420776], [3.096421, 43.420614], [3.096635, 43.420506], [3.096941, 43.421140], [3.095223, 43.421390]]]}},
        "P_26": {"nom": "Vio Cabane Alazet", "cepage": "Viognier", "surface": 1.3, "annee": 2015, "lat": 43.4210, "lon": 3.0940, "geometry": {"type": "Polygon", "coordinates": [[[3.095167, 43.421363], [3.092900, 43.421680], [3.092529, 43.420627], [3.093198, 43.420992], [3.093764, 43.421073], [3.095046, 43.420776], [3.095167, 43.421363]]]}},
        "P_27": {"nom": "Merlot Alazet", "cepage": "Merlot", "surface": 0.45, "annee": 2000, "lat": 43.4210, "lon": 3.0922, "geometry": {"type": "Polygon", "coordinates": [[[3.092566, 43.421754], [3.092204, 43.420938], [3.092129, 43.420661], [3.092194, 43.420398], [3.092529, 43.420668], [3.092900, 43.421707], [3.092566, 43.421754]]]}},
        "P_28": {"nom": "Albarino Brunaude ", "cepage": "Albarino", "surface": 1.09, "annee": 2000, "lat": 43.4220, "lon": 3.0915, "geometry": {"type": "Polygon", "coordinates": [[[3.090506, 43.422866], [3.090032, 43.422326], [3.092289, 43.421334], [3.092549, 43.421955], [3.092215, 43.422009], [3.091834, 43.422029], [3.090506, 43.422866]]]}},
        "P_29": {"nom": "CF Brunaude", "cepage": "Cabernet Franc", "surface": 0.69, "annee": 2000, "lat": 43.4205, "lon": 3.0910, "geometry": {"type": "Polygon", "coordinates": [[[3.090520, 43.420806], [3.090084, 43.420165], [3.090976, 43.419834], [3.091607, 43.420412], [3.090520, 43.420806]]]}},
        "P_30": {"nom": "La Brunaude", "cepage": "Viognier", "surface": 0.83, "annee": 2015, "lat": 43.4218, "lon": 3.0910, "geometry": {"type": "Polygon", "coordinates": [[[3.090075, 43.422267], [3.089926, 43.421964], [3.092118, 43.421073], [3.092286, 43.421356], [3.090075, 43.422267]]]}},
        "P_31": {"nom": "Plantier Viognier Brunaude", "cepage": "Viognier", "surface": 0.75, "annee": 2015, "lat": 43.4215, "lon": 3.0910, "geometry": {"type": "Polygon", "coordinates": [[[3.089926, 43.421937], [3.089833, 43.421579], [3.091988, 43.420749], [3.092118, 43.421066], [3.089926, 43.421937]]]}},
        "P_32": {"nom": "Vio plantier JL", "cepage": "Viognier", "surface": 2.54, "annee": 2000, "lat": 43.4000, "lon": 3.1161, "geometry": {"type": "Polygon", "coordinates": [[[3.114251, 43.399608], [3.116997, 43.399639], [3.118252, 43.400294], [3.114937, 43.400652], [3.114251, 43.399608]]]}},
        "P_33": {"nom": "Chardo JL", "cepage": "Chardonnay", "surface": 2.71, "annee": 2000, "lat": 43.4008, "lon": 3.1171, "geometry": {"type": "Polygon", "coordinates": [[[3.114922, 43.400687], [3.118285, 43.400297], [3.118854, 43.400710], [3.118318, 43.401185], [3.115405, 43.401506], [3.114922, 43.400687]]]}},
        "P_34": {"nom": "Albarino Baysanis", "cepage": "Albarino", "surface": 3.27, "annee": 2000, "lat": 43.3988, "lon": 3.1151, "geometry": {"type": "Polygon", "coordinates": [[[3.113463, 43.399425], [3.113249, 43.398614], [3.113957, 43.398583], [3.114461, 43.398341], [3.115083, 43.398372], [3.115727, 43.398263], [3.115931, 43.398365], [3.116650, 43.398248], [3.116950, 43.399448], [3.116027, 43.399565], [3.113463, 43.399425]]]}},
        "P_35": {"nom": "Chardonnay pentu", "cepage": "Chardonnay", "surface": 0.87, "annee": 2000, "lat": 43.3976, "lon": 3.1172, "geometry": {"type": "Polygon", "coordinates": [[[3.116398, 43.398077], [3.116226, 43.397562], [3.118115, 43.397094], [3.118243, 43.397453], [3.117525, 43.397734], [3.117407, 43.397968], [3.117031, 43.397968], [3.116398, 43.398077]]]}},
        "P_36": {"nom": "Chardonnay Gauphine", "cepage": "Chardonnay", "surface": 3.01, "annee": 2000, "lat": 43.3981, "lon": 3.1181, "geometry": {"type": "Polygon", "coordinates": [[[3.117044, 43.399543], [3.116730, 43.398156], [3.117524, 43.398071], [3.117695, 43.397790], [3.118404, 43.397572], [3.118586, 43.397790], [3.119219, 43.397595], [3.119605, 43.398624], [3.117044, 43.399543]]]}},
        "P_37": {"nom": "Marselan Gauphine", "cepage": "Marselan", "surface": 2.78, "annee": 2000, "lat": 43.4002, "lon": 3.1203, "geometry": {"type": "Polygon", "coordinates": [[[3.117148, 43.399617], [3.119680, 43.398619], [3.119926, 43.399204], [3.120409, 43.399422], [3.120409, 43.399625], [3.119980, 43.399586], [3.119755, 43.399742], [3.120313, 43.400272], [3.120581, 43.400264], [3.121654, 43.401075], [3.122426, 43.401293], [3.122759, 43.401582], [3.122490, 43.401683], [3.120323, 43.401285], [3.117148, 43.399617]]]}},
        "P_38": {"nom": "Syrah Gauphine JL", "cepage": "Syrah", "surface": 4.11, "annee": 2000, "lat": 43.4019, "lon": 3.1210, "geometry": {"type": "Polygon", "coordinates": [[[3.119017, 43.400675], [3.120347, 43.401322], [3.122364, 43.401728], [3.123663, 43.402507], [3.123180, 43.402718], [3.122364, 43.402632], [3.121882, 43.402741], [3.121420, 43.402530], [3.120723, 43.402671], [3.120272, 43.402562], [3.119714, 43.402616], [3.118867, 43.400878], [3.119017, 43.400675]]]}},
        "P_39": {"nom": "Marselan du fond", "cepage": "Marselan", "surface": 0.97, "annee": 2000, "lat": 43.4027, "lon": 3.1243, "geometry": {"type": "Polygon", "coordinates": [[[3.123247, 43.402712], [3.123703, 43.402509], [3.124274, 43.402878], [3.124720, 43.402091], [3.125376, 43.402210], [3.125362, 43.402490], [3.125091, 43.403154], [3.124384, 43.403086], [3.124256, 43.403195], [3.123763, 43.403066], [3.123247, 43.402712]]]}},
        "P_40": {"nom": "Chardonnay 2012", "cepage": "Chardonnay", "surface": 4.53, "annee": 2012, "lat": 43.4039, "lon": 3.1170, "geometry": {"type": "Polygon", "coordinates": [[[3.116529, 43.405528], [3.114818, 43.404782], [3.116529, 43.402772], [3.119013, 43.402964], [3.118994, 43.403091], [3.117791, 43.403489], [3.117556, 43.403496], [3.117615, 43.403795], [3.117507, 43.403965], [3.117497, 43.404214], [3.117009, 43.404576], [3.117126, 43.404868], [3.116529, 43.405528]]]}},
        "P_41": {"nom": "Chardonnay 2011", "cepage": "Chardonnay", "surface": 2.53, "annee": 2014, "lat": 43.4058, "lon": 3.1155, "geometry": {"type": "Polygon", "coordinates": [[[3.113909, 43.405819], [3.114805, 43.404794], [3.116506, 43.405519], [3.116633, 43.405803], [3.116320, 43.406151], [3.115694, 43.406307], [3.115352, 43.406798], [3.113909, 43.405819]]]}},
        "P_42": {"nom": "Gauphine albarino", "cepage": "Albarino", "surface": 1.84, "annee": 2000, "lat": 43.4041, "lon": 3.1148, "geometry": {"type": "Polygon", "coordinates": [[[3.113726, 43.405831], [3.113306, 43.405412], [3.115917, 43.402578], [3.116464, 43.402798], [3.113726, 43.405831]]]}},
        "P_43": {"nom": "Vio fournic Bas JL", "cepage": "Viognier", "surface": 2.28, "annee": 2000, "lat": 43.4036, "lon": 3.1137, "geometry": {"type": "Polygon", "coordinates": [[[3.113704, 43.404729], [3.112443, 43.403564], [3.113929, 43.402747], [3.114866, 43.403563], [3.113704, 43.404729]]]}},
        "P_44": {"nom": "Albarino fournic", "cepage": "Albarino", "surface": 0.46, "annee": 2000, "lat": 43.4038, "lon": 3.1101, "geometry": {"type": "Polygon", "coordinates": [[[3.110436, 43.404636], [3.109468, 43.403130], [3.109908, 43.403123], [3.110759, 43.404437], [3.110436, 43.404636]]]}},
        "P_45": {"nom": "Albarino Cortes", "cepage": "Albarino", "surface": 1.24, "annee": 2000, "lat": 43.4041, "lon": 3.1092, "geometry": {"type": "Polygon", "coordinates": [[[3.109499, 43.404650], [3.109196, 43.404787], [3.108198, 43.403553], [3.109419, 43.403102], [3.110091, 43.404125], [3.109369, 43.404356], [3.109499, 43.404650]]]}},
        "P_46": {"nom": "Marselan Sainte Lucie", "cepage": "Marselan", "surface": 1.23, "annee": 2000, "lat": 43.4396, "lon": 3.0766, "geometry": {"type": "Polygon", "coordinates": [[[3.076447, 43.440507], [3.075437, 43.439996], [3.076252, 43.439207], [3.076691, 43.439379], [3.076886, 43.439318], [3.077561, 43.439571], [3.077053, 43.439895], [3.076447, 43.440507]]]}},
        "P_47": {"nom": "Chardo TRP petite", "cepage": "Chardonnay", "surface": 0.32, "annee": 2000, "lat": 43.4392, "lon": 3.0745, "geometry": {"type": "Polygon", "coordinates": [[[3.074629, 43.439581], [3.074086, 43.439263], [3.074462, 43.438863], [3.075068, 43.439187], [3.074629, 43.439581]]]}},
        "P_48": {"nom": "Chardo Sainte Lucie", "cepage": "Chardonnay", "surface": 3.20, "annee": 2000, "lat": 43.4407, "lon": 3.0746, "geometry": {"type": "Polygon", "coordinates": [[[3.074170, 43.441830], [3.073097, 43.440747], [3.074881, 43.439761], [3.076504, 43.440651], [3.074170, 43.441830]]]}},
        "P_49": {"nom": "Chardo TRP grande", "cepage": "Chardonnay", "surface": 2.27, "annee": 2000, "lat": 43.4394, "lon": 3.0736, "geometry": {"type": "Polygon", "coordinates": [[[3.073573, 43.440466], [3.072110, 43.439318], [3.073211, 43.438509], [3.074249, 43.439065], [3.074074, 43.439328], [3.074855, 43.439778], [3.073573, 43.440466]]]}},
        "P_50": {"nom": "Albarino sainte Lucie ruine", "cepage": "Albarino", "surface": 0.25, "annee": 2000, "lat": 43.4387, "lon": 3.0720, "geometry": {"type": "Polygon", "coordinates": [[[3.072281, 43.439080], [3.071564, 43.438695], [3.071905, 43.438382], [3.072623, 43.438781], [3.072281, 43.439080]]]}},
        "P_51": {"nom": "Syrah Sainte Lucie", "cepage": "Syrah", "surface": 5.80, "annee": 2000, "lat": 43.4411, "lon": 3.0715, "geometry": {"type": "Polygon", "coordinates": [[[3.074048, 43.441980], [3.072834, 43.442608], [3.071222, 43.441123], [3.070518, 43.441517], [3.069270, 43.440445], [3.071095, 43.438997], [3.074048, 43.441980]]]}},
        "P_52": {"nom": "Cinsault Iris", "cepage": "Cinsault", "surface": 2.02, "annee": 2000, "lat": 43.4420, "lon": 3.0704, "geometry": {"type": "Polygon", "coordinates": [[[3.071831, 43.441849], [3.069595, 43.443048], [3.069120, 43.442278], [3.071171, 43.441154], [3.071831, 43.441849]]]}},
        "P_53": {"nom": "Albarino Iris", "cepage": "Albarino", "surface": 1.12, "annee": 2000, "lat": 43.4426, "lon": 3.0712, "geometry": {"type": "Polygon", "coordinates": [[[3.072596, 43.442537], [3.072302, 43.442668], [3.069721, 43.443108], [3.069591, 43.443053], [3.071866, 43.441817], [3.072596, 43.442537]]]}},
        "P_54": {"nom": "Cinsault Rivière", "cepage": "Cinsault", "surface": 1.82, "annee": 2000, "lat": 43.4428, "lon": 3.0744, "geometry": {"type": "Polygon", "coordinates": [[[3.072976, 43.442628], [3.074008, 43.442078], [3.075795, 43.442807], [3.075086, 43.443702], [3.072976, 43.442628]]]}},
        "P_55": {"nom": "Chardo oliviers", "cepage": "Chardonnay", "surface": 1.22, "annee": 2000, "lat": 43.4143, "lon": 3.1036, "geometry": {"type": "Polygon", "coordinates": [[[3.103177, 43.415159], [3.102443, 43.414235], [3.103877, 43.413633], [3.104292, 43.413702], [3.104550, 43.413979], [3.103388, 43.414739], [3.103544, 43.414951], [3.103177, 43.415159]]]}},
        "P_56": {"nom": "Cabernet thézanel", "cepage": "Cabernet Franc", "surface": 1.32, "annee": 2000, "lat": 43.4149, "lon": 3.1021, "geometry": {"type": "Polygon", "coordinates": [[[3.101761, 43.415717], [3.101312, 43.414630], [3.102298, 43.414166], [3.103100, 43.415218], [3.101761, 43.415717]]]}},
        "P_57": {"nom": "Santa fee vieille", "cepage": "Autre", "surface": 1.10, "annee": 2000, "lat": 43.4154, "lon": 3.1004, "geometry": {"type": "Polygon", "coordinates": [[[3.100884, 43.415810], [3.099565, 43.415784], [3.099388, 43.415401], [3.101074, 43.414630], [3.101414, 43.415554], [3.100884, 43.415810]]]}},
        "P_58": {"nom": "Chardo le puit Thezanel", "cepage": "Chardonnay", "surface": 0.54, "annee": 2000, "lat": 43.4161, "lon": 3.0993, "geometry": {"type": "Polygon", "coordinates": [[[3.099598, 43.416971], [3.098857, 43.415417], [3.099250, 43.415364], [3.100019, 43.416826], [3.099598, 43.416971]]]}},
        "P_59": {"nom": "Chardo jeune", "cepage": "Chardonnay", "surface": 0.75, "annee": 2000, "lat": 43.4152, "lon": 3.1045, "geometry": {"type": "Polygon", "coordinates": [[[3.104733, 43.415938], [3.103813, 43.415081], [3.104236, 43.414750], [3.105197, 43.415693], [3.104733, 43.415938]]]}},
        "P_60": {"nom": "Grand Banc et extension", "cepage": "Syrah", "surface": 1.16, "annee": 2000, "lat": 43.4158, "lon": 3.1034, "geometry": {"type": "Polygon", "coordinates": [[[3.103371, 43.416769], [3.102896, 43.416011], [3.102926, 43.415841], [3.103731, 43.415585], [3.103472, 43.415278], [3.103824, 43.415092], [3.104748, 43.415963], [3.103371, 43.416769]]]}},
        "P_61": {"nom": "Chardo derrière maison", "cepage": "Chardonnay", "surface": 0.55, "annee": 2000, "lat": 43.4164, "lon": 3.1025, "geometry": {"type": "Polygon", "coordinates": [[[3.103292, 43.416781], [3.102761, 43.416843], [3.102115, 43.416358], [3.102095, 43.416105], [3.102699, 43.415903], [3.103292, 43.416781]]]}},
        "P_62": {"nom": "Chardo Bergerie", "cepage": "Chardonnay", "surface": 0.70, "annee": 2000, "lat": 43.4175, "lon": 3.1018, "geometry": {"type": "Polygon", "coordinates": [[[3.102129, 43.417095], [3.102798, 43.417157], [3.101689, 43.418087], [3.100963, 43.418075], [3.102129, 43.417095]]]}},
        "P_63": {"nom": "Syrah défriche", "cepage": "Syrah", "surface": 3.18, "annee": 2000, "lat": 43.4206, "lon": 3.1036, "geometry": {"type": "Polygon", "coordinates": [[[3.102902, 43.421980], [3.102020, 43.421111], [3.103407, 43.420379], [3.104164, 43.419419], [3.105171, 43.420288], [3.104478, 43.421203], [3.102902, 43.421980]]]}}
    }

    DATA_PRODUITS = {
        # --- FONGICIDES / INSECTICIDES / HERBICIDES ---
        "Ampexio": {"unite": "kg/ha", "dose_ref": 0.0, "cible": "Mildiou", "type": "Chimie", "ift": True},
        "Ancolie": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Ceremonia": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Chelonia": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Enervin Active + Epetax": {"unite": "kg/ha", "dose_ref": 0.0, "cible": "Mildiou", "type": "Chimie", "ift": True},
        "Epatan": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Etonan": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Hoggar": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Helisol": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Hidalgo": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Idaho": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Karate": {"unite": "L/ha", "dose_ref": 0.0, "cible": "Insecticide", "type": "Chimie", "ift": True},
        "Kesys": {"unite": "kg/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Klartan": {"unite": "L/ha", "dose_ref": 0.0, "cible": "Insecticide", "type": "Chimie", "ift": True},
        "Luna": {"unite": "L/ha", "dose_ref": 0.0, "cible": "Oïdium", "type": "Chimie", "ift": True},
        "Silfet": {"unite": "L/ha", "dose_ref": 0.0, "cible": "Adjuvant", "type": "Chimie", "ift": False}, 
        "Yaris": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},
        "Zelavia": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Chimie", "ift": True},

        # --- CUIVRE & SOUFRE ---
        "BB (Bouillie Bordelaise)": {"unite": "kg/ha", "dose_ref": 0.0, "cible": "Mildiou", "type": "Biocontrôle", "ift": False},
        "Bouillie B": {"unite": "kg/ha", "dose_ref": 0.0, "cible": "Mildiou", "type": "Biocontrôle", "ift": False},
        "Helioterpen Soufre": {"unite": "L/ha", "dose_ref": 0.0, "cible": "Oïdium", "type": "Biocontrôle", "ift": False},
        
        # --- BIOSTIMULANTS / ADJUVANTS ---
        "Flavinc": {"unite": "L/ha", "dose_ref": 0.0, "cible": "?", "type": "Biocontrôle", "ift": False},
        "Helioterpen": {"unite": "L/ha", "dose_ref": 0.0, "cible": "Adjuvant", "type": "Biocontrôle", "ift": False},
        "Pro Act": {"unite": "L/ha", "dose_ref": 0.0, "cible": "Stimulateur", "type": "Biocontrôle", "ift": False},

        # --- ENGRAIS FOLIAIRES / NUTRITION ---
        "Brecil Combi": {"unite": "kg/ha", "dose_ref": 0.0, "cible": "Carence", "type": "Engrais", "ift": False},
        "Calfruit": {"unite": "L/ha", "dose_ref": 0.0, "cible": "Calcium", "type": "Engrais", "ift": False},
        "Nitrates Mg": {"unite": "kg/ha", "dose_ref": 0.0, "cible": "Magnésium", "type": "Engrais", "ift": False},
        "Urie": {"unite": "kg/ha", "dose_ref": 0.0, "cible": "Azote", "type": "Engrais", "ift": False},
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
        ]
        
        for code in DATA_PARCELLES.keys():
            for i, t in enumerate(tasks_template):
                initial_data.append({
                    "id": f"{code}_init_{i}", "parcelle_id": code, "tache": t["tache"], "categorie": t["cat"], 
                    "start": t["start"], "end": t["end"], "statut": t["statut"], "cadence": 1.0, 
                    "jours_estimes": 0.0, "materiel": "Standard", "color_hex": t["color"], "ift_value": 0.0
                })
        return initial_data

def save_data():
    if "db_itk" in st.session_state:
        pd.DataFrame(st.session_state.db_itk).to_csv(CSV_FILE, index=False)

if "db_itk" not in st.session_state:
    st.session_state.db_itk = load_data()


# --- 3. CARTE ---
st.subheader("🗺️ Carte du Vignoble")

def generate_map():
    avg_lat = sum([d['lat'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    avg_lon = sum([d['lon'] for d in DATA_PARCELLES.values()]) / len(DATA_PARCELLES)
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=16)
    
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri', name='Esri Satellite', overlay=False, control=True
    ).add_to(m)
    
    for code, info in DATA_PARCELLES.items():
        if "geometry" in info:
            folium.GeoJson(
                info["geometry"],
                style_function=lambda x, c=info.get("color","gray"): {
                    'fillColor': c, 'color': 'white', 'weight': 1, 'fillOpacity': 0.5
                },
                tooltip=f"{info['nom']} ({info['surface']} ha)"
            ).add_to(m)
        
        folium.map.Marker(
            [info["lat"], info["lon"]],
            icon=folium.DivIcon(
                icon_size=(150, 36), icon_anchor=(75, 18),
                html=f"""<div style="font-size: 11px; font-weight: bold; color: white; text-shadow: 2px 2px 4px #000000; text-align: center; white-space: nowrap; pointer-events: none;">{info['nom']}</div>"""
            )
        ).add_to(m)
        
        folium.CircleMarker(
            [info["lat"], info["lon"]], radius=15, fill_color=info.get("color","gray"), fill_opacity=0.0, stroke=False
        ).add_to(m)

    return m

m = generate_map()
col_map, col_legend = st.columns([5, 1])

with col_map:
    map_output = st_folium(m, height=550, use_container_width=True)

with col_legend:
    st.markdown("**Légende**")
    for cepage, color in COLOR_MAP.items():
        st.markdown(f"<span style='color:{color};'>■</span> {cepage}", unsafe_allow_html=True)

selected_code_map = None
if map_output["last_object_clicked"]:
    lat_clic = map_output["last_object_clicked"]["lat"]
    lon_clic = map_output["last_object_clicked"]["lng"]
    min_dist = 1000
    closest_code = None
    for code, info in DATA_PARCELLES.items():
        dist = ((info["lat"] - lat_clic)**2 + (info["lon"] - lon_clic)**2)**0.5
        if dist < 0.003: 
            if dist < min_dist:
                min_dist = dist
                closest_code = code
    if closest_code: selected_code_map = closest_code

# --- 4. ONGLETS PRINCIPAUX ---
st.divider()
tab_view, tab_plan, tab_phyto, tab_stats, tab_data = st.tabs(["🔍 Détail Parcelle", "🚜 Planif Groupée", "🧪 Traitements Phyto", "📊 Statistiques", "🗃️ Data"])

# =========================================================
# ONGLET 1 : DÉTAIL PARCELLE
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
            df_filtered["duree_calc"] = (df_filtered["end"] - df_filtered["start"]).dt.days + 1
            df_filtered["start_txt"] = df_filtered["start"].dt.strftime('%d/%m/%Y')
            df_filtered["end_txt"] = df_filtered["end"].dt.strftime('%d/%m/%Y')

            color_map_gantt = {row["tache"]: row["color_hex"] for index, row in df_filtered.iterrows()}
            
            fig = px.timeline(
                df_filtered, x_start="start", x_end="end", y="tache", color="tache",
                color_discrete_map=color_map_gantt, title="Planning des travaux",
                custom_data=["start_txt", "end_txt", "duree_calc", "statut"]
            )
            fig.update_traces(hovertemplate=("<b>%{y}</b><br>📅 Du %{customdata[0]} au %{customdata[1]}<br>⏳ Durée : <b>%{customdata[2]} jours</b><br>📌 Statut : %{customdata[3]}<extra></extra>"))

            aujourdhui = pd.Timestamp(date.today())
            fig.add_vline(x=aujourdhui, line_width=2, line_dash="dash", line_color="#e74c3c")
            fig.add_annotation(x=aujourdhui, y=1.05, yref="paper", text="📍 Aujourd'hui", showarrow=False, font=dict(color="#e74c3c", size=12))
            fig.update_yaxes(autorange="reversed", title="")
            fig.update_layout(xaxis=dict(range=[date(date.today().year, 1, 1), date(date.today().year, 12, 31)]))
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.caption("Pour modifier/supprimer une tâche standard :")
            task_options = df_filtered[df_filtered["categorie"] != "Traitements"].to_dict('records') 
            
            if task_options:
                def format_func(task): return f"{task['tache']} ({task.get('start_txt', '?')})"
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
                        del_chk = st.checkbox("Supprimer cette tâche ?")
                        
                        if st.form_submit_button("Enregistrer les modifications"):
                            if del_chk:
                                del st.session_state.db_itk[real_index]
                                st.success("Tâche supprimée !")
                            else:
                                st.session_state.db_itk[real_index].update({"statut": ns, "color_hex": nc, "start": d1, "end": d2})
                                st.success("Mise à jour effectuée !")
                            save_data()
                            st.rerun()
            else:
                st.info("Aucune tâche standard modifiable.")
        else:
            st.info("Aucune intervention planifiée sur cette parcelle.")
    else:
        st.info("👆 Cliquez sur une parcelle sur la carte pour voir le détail.")

# =========================================================
# ONGLET 2 : PLANIF GROUPÉE
# =========================================================
with tab_plan:
    st.subheader("🛠️ Ajouter une intervention (Sauf Phyto)")
    c_g, c_d = st.columns([1, 2])
    
    with c_g:
        sorted_keys = sorted(DATA_PARCELLES.keys(), key=lambda x: DATA_PARCELLES[x]['nom'])

        # --- LOGIQUE TOUT SELECTIONNER (CORRIGÉE) ---
        def toggle_all_planif():
            if st.session_state.get("chk_all_planif"):
                st.session_state["multi_planif"] = sorted_keys
            else:
                st.session_state["multi_planif"] = []

        st.checkbox("✅ Tout sélectionner", key="chk_all_planif", on_change=toggle_all_planif)

        sel_ids = st.multiselect(
            "Rechercher & Sélectionner les parcelles", 
            options=sorted_keys, 
            format_func=lambda x: DATA_PARCELLES[x]['nom'],
            key="multi_planif" # Clé importante pour le callback
        )
        
        surf = sum([DATA_PARCELLES[p]['surface'] for p in sel_ids])
        st.info(f"📐 Surface sélectionnée : **{surf:.2f} ha**")
        st.write("---")
        st.markdown("**Calculateur de temps**")
        
        # Saisie clavier (step=0.0)
        cad = st.number_input("Cadence (h/ha)", min_value=0.0, value=10.0, step=0.0)
        nb_p = st.number_input("Nb Pers", min_value=1, value=1, step=1)
        
        if surf > 0 and cad > 0:
            heures_tot = surf * cad
            j_est = heures_tot / (nb_p * 7)
            st.caption(f"Total heures : {heures_tot:.1f} h")
            st.success(f"⏳ Durée estimée : **{j_est:.1f} jours** (à {nb_p} pers)")
        else:
            j_est = 1.0

    with c_d:
        st.markdown("#### 📝 Détails de l'intervention")
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
            d2 = st.date_input("Fin", d1 + timedelta(days=int(j_est) if j_est>=1 else 0))
            
            if st.form_submit_button("✅ Valider l'ajout"):
                if sel_ids:
                    ts = datetime.now().timestamp()
                    for pid in sel_ids:
                        st.session_state.db_itk.append({
                            "id": f"{pid}_{ts}", "parcelle_id": pid, "tache": n_t, "categorie": n_c,
                            "start": d1, "end": d2, "statut": n_s, "cadence": cad, "jours_estimes": j_est,
                            "materiel": n_m, "color_hex": n_col, "ift_value": 0.0
                        })
                    save_data()
                    st.success(f"Tâche ajoutée sur {len(sel_ids)} parcelles !")
                    st.rerun()
                else:
                    st.error("Veuillez sélectionner au moins une parcelle.")

# =========================================================
# ONGLET 3 : TRAITEMENTS PHYTO
# =========================================================
with tab_phyto:
    st.subheader("🧪 Traitements & Calcul IFT")

    with st.expander("Voir l'historique des traitements", expanded=False):
        df_all_phyto = pd.DataFrame(st.session_state.db_itk)
        if not df_all_phyto.empty and "categorie" in df_all_phyto.columns:
            df_phyto = df_all_phyto[df_all_phyto["categorie"] == "Traitements"].copy()
            if not df_phyto.empty:
                df_phyto["start"] = pd.to_datetime(df_phyto["start"])
                st.dataframe(df_phyto[["start", "tache", "materiel", "ift_value"]].sort_values("start", ascending=False), use_container_width=True)
            else:
                st.info("Aucun traitement.")

    st.divider()

    c_left, c_right = st.columns([1, 1.5])
    if "current_mix" not in st.session_state: st.session_state.current_mix = []

    with c_left:
        st.markdown("#### 1. Configuration du Chantier")
        with st.container(border=True):
            sorted_keys = sorted(DATA_PARCELLES.keys(), key=lambda x: DATA_PARCELLES[x]['nom'])
            
            # --- LOGIQUE TOUT SELECTIONNER (CORRIGÉE) ---
            def toggle_all_phyto():
                if st.session_state.get("chk_all_phyto"):
                    st.session_state["multi_phyto"] = sorted_keys
                else:
                    st.session_state["multi_phyto"] = []

            st.checkbox("✅ Tout sélectionner", key="chk_all_phyto", on_change=toggle_all_phyto)

            sel_parc = st.multiselect(
                "Parcelles à traiter", options=sorted_keys, format_func=lambda x: DATA_PARCELLES[x]['nom'],
                key="multi_phyto" # Clé pour le callback
            )
            
            surf_tot = sum([DATA_PARCELLES[p]['surface'] for p in sel_parc])
            if surf_tot > 0:
                st.success(f"📐 Surface Totale : **{surf_tot:.2f} ha**")
            else:
                st.warning("Sélectionnez des parcelles.")

            st.write("---")
            d_app = st.date_input("Date", date.today())
            n_app = st.text_input("Nom du Traitement", value="T... Mildiou", key="nom_traitement_input")
            
            # Saisie clavier sans flèches (step=0.0)
            vol_ha_cible = st.number_input("Volume Bouillie (L/ha)", value=150.0, step=0.0, format="%.0f") 
            st.caption(f"💧 Eau requise : **{surf_tot * vol_ha_cible:.0f} Litres**")

    with c_right:
        st.markdown("#### 2. Composition & IFT")
        
        if surf_tot > 0:
            with st.form("add_product_form", clear_on_submit=True):
                st.caption("Ajoutez les produits un par un.")
                c_p1, c_p2 = st.columns([1.5, 1])
                
                with c_p1:
                    choix_prod = st.selectbox("Produit", list(DATA_PRODUITS.keys()) + ["✍️ Autre / Nouveau..."])
                    
                    nom_final = choix_prod
                    dose_ref_val = 1.0 
                    unite_val = "kg/L"
                    
                    if choix_prod == "✍️ Autre / Nouveau...":
                        nom_final = st.text_input("Nom du produit", value="Nouveau Produit")
                        # Saisie clavier Dose Réf (Nouveau Produit)
                        dose_ref_val = st.number_input("Dose Homologuée (Référence IFT=1)", min_value=0.01, value=1.0, step=0.0, format="%.2f")
                        unite_val = st.text_input("Unité", "L/ha")
                    else:
                        # CAS EXISTANT : Lecture Seule (Protection des données)
                        infos = DATA_PRODUITS[choix_prod]
                        dose_ref_val = float(infos['dose_ref'])
                        unite_val = infos['unite']
                        st.markdown(f"**Dose Réf (IFT=1) :** `{dose_ref_val} {unite_val}`")

                with c_p2:
                    # Saisie clavier Dose Appliquée (step=0.0)
                    dose_app = st.number_input(f"Votre Dose / ha", min_value=0.0, value=0.0, step=0.0, format="%.2f")
                    
                    ift_calc = 0.0
                    if dose_ref_val > 0 and dose_app > 0:
                        ift_calc = dose_app / dose_ref_val
                    
                    if ift_calc > 0: st.caption(f"IFT : {ift_calc:.2f}")

                ajout = st.form_submit_button("➕ Ajouter au mélange")
                
                if ajout:
                    if dose_app > 0:
                        qte_cuve = dose_app * surf_tot
                        st.session_state.current_mix.append({
                            "produit": nom_final, "dose_app": dose_app, "dose_ref": dose_ref_val,
                            "qte_cuve": qte_cuve, "unite": unite_val, "ift": ift_calc
                        })
                        st.rerun()
                    else:
                        st.error("La dose doit être supérieure à 0.")

            if st.session_state.current_mix:
                st.markdown("##### 📋 Contenu de la Cuve")
                df_mix = pd.DataFrame(st.session_state.current_mix)
                ift_total_traitement = df_mix["ift"].sum()
                
                df_display = df_mix.rename(columns={"produit": "Produit", "dose_app": "Dose/ha", "qte_cuve": "QTÉ CUVE", "ift": "IFT"})
                st.dataframe(df_display[["Produit", "Dose/ha", "QTÉ CUVE", "IFT"]], use_container_width=True, hide_index=True)
                st.metric("IFT TOTAL DU TRAITEMENT", f"{ift_total_traitement:.2f}")
                
                c_val, c_reset = st.columns([3, 1])
                with c_val:
                    if st.button("✅ ENREGISTRER TRAITEMENT", type="primary"):
                        ts = datetime.now().timestamp()
                        desc_parts = [f"{row['produit']} ({row['dose_app']}{row['unite']})" for i, row in df_mix.iterrows()]
                        desc_full = f"Vol:{vol_ha_cible}L | " + " + ".join(desc_parts)
                        
                        for pid in sel_parc:
                            st.session_state.db_itk.append({
                                "id": f"{pid}_phy_{ts}", "parcelle_id": pid, "tache": n_app,
                                "categorie": "Traitements", "start": d_app, "end": d_app,
                                "statut": "Fini", "color_hex": "#8e44ad", "ift_value": ift_total_traitement,
                                "materiel": desc_full, "jours_estimes": 0.5
                            })
                        save_data()
                        st.session_state.current_mix = []
                        st.success(f"Enregistré ! IFT Total : {ift_total_traitement:.2f}")
                        st.rerun()
                
                with c_reset:
                    if st.button("🗑️ Vider"):
                        st.session_state.current_mix = []
                        st.rerun()
        else:
            st.info("👈 Sélectionnez des parcelles.")
            
    with st.expander("🛠️ Modifier / Supprimer un ancien traitement"):
        all_phyto_list = [t for t in st.session_state.db_itk if t.get("categorie") == "Traitements"]
        if all_phyto_list:
            all_phyto_list.sort(key=lambda x: x['start'], reverse=True)
            def fmt_p(x):
                pname = DATA_PARCELLES.get(x['parcelle_id'], {}).get('nom', '?')
                return f"{x['start']} | {pname} | {x['tache']} (IFT: {x.get('ift_value', 0):.2f})"

            sel_edit_phy = st.selectbox("Choisir un traitement", all_phyto_list, format_func=fmt_p)
            if sel_edit_phy:
                idx_phy = next((i for i, item in enumerate(st.session_state.db_itk) if item["id"] == sel_edit_phy["id"]), -1)
                with st.form("edit_phyto_form"):
                    new_n = st.text_input("Nom", sel_edit_phy['tache'])
                    new_ift = st.number_input("IFT", value=float(sel_edit_phy.get('ift_value', 0.0)), step=0.0, format="%.2f")
                    del_phy = st.checkbox("Supprimer définitivement ?")
                    if st.form_submit_button("Mettre à jour"):
                        if del_phy:
                            del st.session_state.db_itk[idx_phy]
                            st.success("Supprimé !")
                        else:
                            st.session_state.db_itk[idx_phy].update({"tache": new_n, "ift_value": new_ift})
                            st.success("Modifié !")
                        save_data()
                        st.rerun()

# =========================================================
# ONGLET 4 : TABLEAU DE BORD
# =========================================================
with tab_stats:
    st.subheader("📊 Tableau de Bord & Pilotage Rapide")
    df_all = pd.DataFrame(st.session_state.db_itk)
    
    if not df_all.empty:
        df_all["start"] = pd.to_datetime(df_all["start"])
        df_all["end"] = pd.to_datetime(df_all["end"])
        today = pd.Timestamp(date.today())
        
        def calc_progress(row):
            if row["statut"] == "Fini": return 100
            if row["statut"] in ["Planifié", "A faire"]: return 0
            total_days = (row["end"] - row["start"]).days + 1
            days_passed = (today - row["start"]).days + 1
            if total_days <= 0: return 0
            return max(0, min(100, (days_passed / total_days) * 100))

        df_all["progress"] = df_all.apply(calc_progress, axis=1)

        st.markdown("#### ⚡ Mise à jour rapide des statuts")
        main_tasks = ["Taille & Tirage", "Enherbement", "Prétaille", "Epandage Compost", "Sécaille/Attachage", "Broyage du bois", "Epandage Engrais", "Désherbage"]
        df_matrix = df_all[df_all["tache"].isin(main_tasks)].copy()
        name_to_id = {info['nom']: code for code, info in DATA_PARCELLES.items()}
        df_matrix["Nom_Parcelle"] = df_matrix["parcelle_id"].apply(lambda x: DATA_PARCELLES.get(x, {}).get("nom", x))

        try:
            pivot_df = df_matrix.pivot(index="Nom_Parcelle", columns="tache", values="statut")
            column_config = {}
            for col in pivot_df.columns:
                column_config[col] = st.column_config.SelectboxColumn(col, options=["Planifié", "A faire", "En cours", "Fini"], required=True, width="medium")

            edited_df = st.data_editor(pivot_df, column_config=column_config, use_container_width=True, height=400, key="editor_stats")

            if not edited_df.equals(pivot_df):
                for nom_parcelle, row in edited_df.iterrows():
                    pid = name_to_id.get(nom_parcelle)
                    if pid:
                        for tache_col in edited_df.columns:
                            new_statut = row[tache_col]
                            for item in st.session_state.db_itk:
                                if item["parcelle_id"] == pid and item["tache"] == tache_col:
                                    if item["statut"] != new_statut:
                                        item["statut"] = new_statut
                save_data()
                st.rerun()
        except Exception as e:
            st.warning(f"Données insuffisantes pour la matrice.")

        st.divider()
        st.markdown("#### ⏳ Chantiers en cours")
        df_running = df_all[df_all["statut"] == "En cours"].copy()
        if not df_running.empty:
            df_running["Nom_Parcelle"] = df_running["parcelle_id"].apply(lambda x: DATA_PARCELLES.get(x, {}).get("nom", x))
            for index, row in df_running.iterrows():
                col_txt, col_bar = st.columns([1, 3])
                with col_txt: st.text(f"{row['Nom_Parcelle']} : {row['tache']}")
                with col_bar:
                    st.progress(int(row['progress']))
                    st.caption(f"📅 Fin : {row['end'].strftime('%d/%m')} ({int(row['progress'])}%)")
        else:
            st.info("Rien en cours.")

        st.divider()
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(px.pie(df_all, names="categorie", hole=0.4), use_container_width=True)
        with c2: st.plotly_chart(px.pie(df_all, names="statut", color="statut", color_discrete_map={"Fini":"green", "En cours":"orange", "A faire":"red", "Planifié":"blue"}), use_container_width=True)
    else:
        st.info("Aucune donnée.")

# ONGLET 5 : DATA
with tab_data:
    st.dataframe(pd.DataFrame(st.session_state.db_itk))