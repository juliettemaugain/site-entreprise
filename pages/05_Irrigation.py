import streamlit as st
import folium
from streamlit_folium import st_folium
import base64
import os

# ====================== 0. CONFIGURATION DE LA PAGE ======================
st.set_page_config(layout="wide", page_title="Irrigation - Domaine Viticole", page_icon="💧")

# ====================== 1. DONNÉES ======================

# --- DONNÉES DES PARCELLES ---
DATA_PARCELLES = {
    "P_00": {"nom": "Syrah Isabelle", "cepage": "Syrah", "surface": 0.56, "annee": 2019, "lat": 43.4290, "lon": 3.0930, "taille": "Palmette", "objectif": "Rosé premium", "irrigation": "Goutte à goutte", "geometry": {"type": "Polygon", "coordinates": [[[3.092493, 43.429614], [3.092055, 43.428946], [3.093490, 43.428517], [3.093604, 43.428660], [3.093541, 43.428766], [3.093464, 43.428844], [3.093363, 43.428914], [3.093242, 43.428914], [3.093128, 43.428932], [3.092595, 43.429582], [3.092493, 43.429614]]]}},
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
        "P_63": {"nom": "Syrah défriche", "cepage": "Syrah", "surface": 3.18, "annee": 2000, "lat": 43.4208, "lon": 3.1035, "geometry": {"type": "Polygon", "coordinates": [[[3.103633, 43.421797], [3.103450, 43.421668], [3.102877, 43.421993], [3.102014, 43.420942], [3.103151, 43.420478], [3.103425, 43.420057], [3.104303, 43.419619], [3.104457, 43.419724], [3.104944, 43.419845], [3.105066, 43.420057], [3.104751, 43.420817], [3.104177, 43.421351], [3.104000, 43.421627], [3.103633, 43.421797]]]}},
        "P_64": {"nom": "Cinsault haut savignac", "cepage": "Cinsault", "surface": 1.77, "annee": 2000, "lat": 43.4196, "lon": 3.1193, "geometry": {"type": "Polygon", "coordinates": [[[3.118926, 43.420432], [3.118775, 43.419959], [3.119068, 43.419912], [3.118738, 43.418549], [3.119982, 43.418350], [3.120390, 43.419447], [3.119702, 43.419844], [3.118926, 43.420432]]]}},
        "P_65": {"nom": "Vio Grand Olivette", "cepage": "Viognier", "surface": 2.28, "annee": 2000, "lat": 43.4183, "lon": 3.1211, "geometry": {"type": "Polygon", "coordinates": [[[3.120438, 43.419460], [3.120004, 43.418406], [3.121135, 43.418214], [3.120654, 43.417063], [3.121409, 43.416981], [3.122012, 43.418556], [3.121663, 43.418741], [3.121126, 43.419392], [3.120438, 43.419460]]]}},
        "P_66": {"nom": "Cinsault haut savignac", "cepage": "Cinsault", "surface": 2.30, "annee": 2000, "lat": 43.4179, "lon": 3.1197, "geometry": {"type": "Polygon", "coordinates": [[[3.121032, 43.418187], [3.118741, 43.418543], [3.118363, 43.417447], [3.120673, 43.417152], [3.121032, 43.418187]]]}},
        "P_67": {"nom": "Cinsault Olivette", "cepage": "Cinsault", "surface": 1.30, "annee": 2000, "lat": 43.4177, "lon": 3.1222, "geometry": {"type": "Polygon", "coordinates": [[[3.122012, 43.418553], [3.121427, 43.417030], [3.122148, 43.416962], [3.122683, 43.417702], [3.122988, 43.417986], [3.122343, 43.418504], [3.122012, 43.418553]]]}},
        "P_68": {"nom": "Viognier Haut Savignac", "cepage": "Viognier", "surface": 1.32, "annee": 2000, "lat": 43.4175, "lon": 3.1167, "geometry": {"type": "Polygon", "coordinates": [[[3.117897, 43.417404], [3.117048, 43.417712], [3.116224, 43.418156], [3.116055, 43.418014], [3.115647, 43.417903], [3.116819, 43.416941], [3.117510, 43.416861], [3.117897, 43.417404]]]}},
        "P_69": {"nom": "Albarino Savignac", "cepage": "Albarino", "surface": 0.99, "annee": 2000, "lat": 43.4198, "lon": 3.1257, "geometry": {"type": "Polygon", "coordinates": [[[3.124936, 43.420401], [3.124688, 43.419785], [3.126084, 43.419401], [3.127046, 43.419760], [3.124936, 43.420401]]]}},
        "P_70": {"nom": "Cinsault Gravière", "cepage": "Cinsault", "surface": 0.91, "annee": 2000, "lat": 43.4185, "lon": 3.1262, "geometry": {"type": "Polygon", "coordinates": [[[3.125391, 43.418948], [3.124729, 43.418625], [3.127128, 43.418002], [3.127532, 43.418377], [3.125391, 43.418948]]]}},
        "P_71": {"nom": "Cinsauit Château", "cepage": "Cinsault", "surface": 1.08, "annee": 2000, "lat": 43.4178, "lon": 3.1243, "geometry": {"type": "Polygon", "coordinates": [[[3.124594, 43.418603], [3.123435, 43.418084], [3.123839, 43.417558], [3.124697, 43.417258], [3.125184, 43.418407], [3.124594, 43.418603]]]}},
        "P_72": {"nom": "Vio Bas Savignac", "cepage": "Viognier", "surface": 6.78, "annee": 2000, "lat": 43.4174, "lon": 3.1270, "geometry": {"type": "Polygon", "coordinates": [[[3.128235, 43.418956], [3.127149, 43.417979], [3.125246, 43.418430], [3.124646, 43.417265], [3.125184, 43.416882], [3.125132, 43.416041], [3.125856, 43.416011], [3.128184, 43.416582], [3.128359, 43.416552], [3.128690, 43.417468], [3.129011, 43.417634], [3.129197, 43.418392], [3.128235, 43.418956]]]}},
        "P_73": {"nom": "Sauv bas Savignac", "cepage": "Sauvignon Blanc", "surface": 1.85, "annee": 2000, "lat": 43.4160, "lon": 3.1245, "geometry": {"type": "Polygon", "coordinates": [[[3.125162, 43.416837], [3.124872, 43.416995], [3.124179, 43.416972], [3.124210, 43.415575], [3.123010, 43.415605], [3.123465, 43.415019], [3.124075, 43.415109], [3.124262, 43.415214], [3.124738, 43.415116], [3.125389, 43.415515], [3.125937, 43.415965], [3.125120, 43.416033], [3.125162, 43.416837]]]}},
        "P_74": {"nom": "Plantier Route", "cepage": "Syrah", "surface": 1.39, "annee": 2000, "lat": 43.4273, "lon": 3.0808, "geometry": {"type": "Polygon", "coordinates": [[[3.081975, 43.427994], [3.080748, 43.427932], [3.080437, 43.427203], [3.079786, 43.427141], [3.079888, 43.426755], [3.081873, 43.426837], [3.081975, 43.427994]]]}},
        "P_75": {"nom": "Mourvèdre berlan", "cepage": "Mourvèdre", "surface": 0.62, "annee": 2000, "lat": 43.4219, "lon": 3.0729, "geometry": {"type": "Polygon", "coordinates": [[[3.072374, 43.422414], [3.071971, 43.421870], [3.073374, 43.421496], [3.073721, 43.421880], [3.072374, 43.422414]]]}},
        "P_76": {"nom": "Plantier Grenache Berlan", "cepage": "Grenache", "surface": 1.44, "annee": 2000, "lat": 43.4222, "lon": 3.0691, "geometry": {"type": "Polygon", "coordinates": [[[3.069412, 43.423029], [3.069190, 43.422898], [3.068965, 43.422485], [3.068682, 43.422398], [3.068270, 43.422235], [3.068659, 43.421604], [3.069318, 43.421799], [3.069438, 43.421696], [3.070337, 43.422120], [3.069880, 43.422849], [3.069412, 43.423029]]]}},
        "P_77": {"nom": "Grenache Berlan", "cepage": "Grenache", "surface": 0.50, "annee": 2000, "lat": 43.4218, "lon": 3.0701, "geometry": {"type": "Polygon", "coordinates": [[[3.069452, 43.421702], [3.069587, 43.421201], [3.070875, 43.421876], [3.070351, 43.422148], [3.069452, 43.421702]]]}},
        "P_78": {"nom": "Grenache Virgule", "cepage": "Grenache", "surface": 0.79, "annee": 2000, "lat": 43.4214, "lon": 3.0677, "geometry": {"type": "Polygon", "coordinates": [[[3.066782, 43.421905], [3.066572, 43.421721], [3.067921, 43.421167], [3.068728, 43.421065], [3.068544, 43.421549], [3.068158, 43.421390], [3.067448, 43.421523], [3.066782, 43.421905]]]}},
        "P_79": {"nom": "Grenache la Jasse", "cepage": "Grenache", "surface": 0.83, "annee": 2000, "lat": 43.4208, "lon": 3.0665, "geometry": {"type": "Polygon", "coordinates": [[[3.067492, 43.421250], [3.066826, 43.421498], [3.065766, 43.420435], [3.066248, 43.420110], [3.067492, 43.421250]]]}},
        "P_80": {"nom": "Grenache Clerc", "cepage": "Grenache", "surface": 0.97, "annee": 2000, "lat": 43.4209, "lon": 3.0691, "geometry": {"type": "Polygon", "coordinates": [[[3.068125, 43.421094], [3.067993, 43.420941], [3.068905, 43.420139], [3.070044, 43.420896], [3.069606, 43.421176], [3.068712, 43.421055], [3.068125, 43.421094]]]}},
        "P_81": {"nom": "Syrah Grande", "cepage": "Syrah", "surface": 0.99, "annee": 2000, "lat": 43.4194, "lon": 3.0674, "geometry": {"type": "Polygon", "coordinates": [[[3.067196, 43.420164], [3.066600, 43.419591], [3.067713, 43.418707], [3.068274, 43.419350], [3.067196, 43.420164]]]}},
        "P_82": {"nom": "Petite Syrah", "cepage": "Syrah", "surface": 0.42, "annee": 2000, "lat": 43.4204, "lon": 3.0698, "geometry": {"type": "Polygon", "coordinates": [[[3.070053, 43.420915], [3.069106, 43.420292], [3.069501, 43.419992], [3.070465, 43.420642], [3.070053, 43.420915]]]}},
        "P_83": {"nom": "Petit Grenache", "cepage": "Grenache", "surface": 0.38, "annee": 2000, "lat": 43.4208, "lon": 3.0714, "geometry": {"type": "Polygon", "coordinates": [[[3.071219, 43.421226], [3.070781, 43.420953], [3.070938, 43.420698], [3.071727, 43.420437], [3.071911, 43.420774], [3.071622, 43.421042], [3.071219, 43.421226]]]}},
        "P_84": {"nom": "Grenache Capel", "cepage": "Grenache", "surface": 1.39, "annee": 2000, "lat": 43.4198, "lon": 3.0705, "geometry": {"type": "Polygon", "coordinates": [[[3.070682, 43.420738], [3.069403, 43.419892], [3.070051, 43.419497], [3.069823, 43.418981], [3.070244, 43.418867], [3.070674, 43.419643], [3.071611, 43.420401], [3.071331, 43.420490], [3.071094, 43.420496], [3.070682, 43.420738]]]}}
        }# ... 
# --- BORNES ET VANNES ---
DATA_BORNES = {
    "A": {
        "nom": "Borne A",
        "coords": [43.430944, 3.094250],
        "debit": 25,
        "pression": 3.5,
        "hectares": 3.5,
        "parcelles": ["Roumanissas", "Nouveau plantier Syrah", "Syrah roumanissas", "Syrah du muscat", "Syrah hébram", "Plantier"],
        "photos": ["images/bornes/B_A_front.jpg", "images/bornes/B_A_side.jpg"],
        "explications": "Ras",
        "statut": "OK",
        "vannes_associées": ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
    },
    "B": {
        "nom": "Borne B",
        "coords": [43.428972, 3.091889],
        "debit": 20,
        "pression": 3.0,
        "hectares": 2.8,
        "parcelles": ["Syrah Isabelle", "Amandier", "Olivette"],
        "photos": ["images/bornes/B_B_front.jpg"],
        "explications": "Borne pour les parcelles Syrah Isabelle et Olivette. Débit modéré pour 2.8 hectares.",
        "statut": "OK",
        "vannes_associées": ["B1", "B2", "B3", "B4"]
    },
    "C": {
        "nom": "Borne C",
        "coords": [43.428528, 3.087639],
        "debit": 25,
        "pression": 3.5,
        "hectares": 3.5,
        "parcelles": ["Hébram", "Calvet", "Caravane", "La Plaine", "Trompet"],
        "photos": ["images/bornes/B_C_front.jpg"],
        "explications": "Borne couvrant les parcelles centrales (Hébram, Calvet). Débit adapté aux 3.5 hectares.",
        "statut": "OK",
        "vannes_associées": ["C1", "C2", "C3", "C4", "C5", "C6", "C7"]
    },
    "D": {
        "nom": "Borne D",
        "coords": [43.425722, 3.094417],
        "debit": 35,
        "pression": 4.0,
        "hectares": 4.9,
        "parcelles": ["Vio Jardin", "Saigne", "Phylloxera", "Alba Coural", "Syrah Coural", "Vio source Romaine", "Viognier Alazet cabane", "Viognier Alazet"],
        "photos": ["images/bornes/B_D_front.jpg"],
        "explications": "Borne avec le débit le plus élevé (35 m³/h) pour couvrir 4.9 hectares. Parcelles variées (Viognier, Syrah).",
        "statut": "OK",
        "vannes_associées": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15"]
    },
    "K": {
        "nom": "Borne K",
        "coords": [43.421944, 3.084639],
        "debit": 20,
        "pression": 3.0,
        "hectares": 2.8,
        "parcelles": ["Grand Bardou", "Petit Bardou", "Plantier terret", "Brunaude Alba", "La Brunaude", "Plantier Vio Brunaude", "CF Brunaude"],
        "photos": ["images/bornes/B_K_front.jpg"],
        "explications": "Borne pour les parcelles Bardou et Brunaude. Débit standard pour 2.8 hectares.",
        "statut": "OK",
        "vannes_associées": ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9", "K10", "K11", "K12", "K13", "K14", "K15", "K16"]
    }
}

DATA_VANNES = {
    "A1": {"nom": "Vanne A1", "lat": 43.431194, "lon": 3.091833, "parcelles_associées": ["Roumanissas"], "ha": 1.9, "borne_associée": "B_A"},
    "A2": {"nom": "Vanne A2", "lat": 43.432278, "lon": 3.090444, "parcelles_associées": ["Syrah rouman"], "ha": 0.46, "borne_associée": "B_A"},
    "A3": {"nom": "Vanne A3", "lat": 43.432278, "lon": 3.090444, "parcelles_associées": ["Nouveau plant"], "ha": 2.22, "borne_associée": "B_A"},
    "A4": {"nom": "Vanne A4", "lat": 43.432278, "lon": 3.090444, "parcelles_associées": ["Nouveau plant"], "ha": 2.22, "borne_associée": "B_A"},
    "A5": {"nom": "Vanne A5", "lat": 43.430944, "lon": 3.092306, "parcelles_associées": ["Plantier"], "ha": 0.3, "borne_associée": "B_A"},
    "A6": {"nom": "Vanne A6", "lat": 43.430500, "lon": 3.089444, "parcelles_associées": ["Syrah du mus"], "ha": 0.63, "borne_associée": "B_A"},
    "A7": {"nom": "Vanne A7", "lat": 43.430500, "lon": 3.089444, "parcelles_associées": ["syrah hébram"], "ha": 0.61, "borne_associée": "B_A"},
    
    "B1": {"nom": "Vanne B1", "lat": 43.428889, "lon": 3.092000, "parcelles_associées": ["Amandier"], "ha": 1.95, "borne_associée": "B_B"},
    "B2": {"nom": "Vanne B2", "lat": 43.428889, "lon": 3.092000, "parcelles_associées": ["Amandier", "Oli"], "ha": 1.95, "borne_associée": "B_B"},
    "B3": {"nom": "Vanne B3", "lat": 43.428889, "lon": 3.092000, "parcelles_associées": ["Olivette"], "ha": 1.95, "borne_associée": "B_B"},
    "B4": {"nom": "Vanne B4", "lat": 43.428889, "lon": 3.092000, "parcelles_associées": ["Syrah Isabelle"], "ha": 0.56, "borne_associée": "B_B"},

    "C1": {"nom": "Vanne C1", "lat": 43.428611, "lon": 3.088028, "parcelles_associées": ["Hébram long"], "ha": 2.0, "borne_associée": "B_C"},
    "C2": {"nom": "Vanne C2", "lat": 43.428611, "lon": 3.088028, "parcelles_associées": ["Hébram court"], "ha": 0.69, "borne_associée": "B_C"},
    "C3": {"nom": "Vanne C3", "lat": 43.428639, "lon": 3.085722, "parcelles_associées": ["Caravane"], "ha": 1.34, "borne_associée": "B_C"},
    "C4": {"nom": "Vanne C4", "lat": 43.428000, "lon": 3.086778, "parcelles_associées": ["Syrah du Virage"], "ha": 0, "borne_associée": "B_C"},
    "C5": {"nom": "Vanne C5", "lat": 43.428000, "lon": 3.086778, "parcelles_associées": ["Calvet"], "ha": 2.03, "borne_associée": "B_C"},
    "C6": {"nom": "Vanne C6", "lat": 43.428000, "lon": 3.086778, "parcelles_associées": ["La Plaine"], "ha": 2.05, "borne_associée": "B_C"},
    "C7": {"nom": "Vanne C7", "lat": 43.426528, "lon": 3.087889, "parcelles_associées": ["Trompet"], "ha": 1.81, "borne_associée": "B_C"},

    "D1": {"nom": "Vanne D1", "lat": 43.426361, "lon": 3.093750, "parcelles_associées": ["Saigne"], "ha": 1.35, "borne_associée": "B_D", "photo": "pages/images/saigne1.jpg"},
    "D2": {"nom": "Vanne D2", "lat": 43.425833, "lon": 3.093028, "parcelles_associées": ["Saigne"], "ha": 1.35, "borne_associée": "B_D", "photo": "pages/images/saigne2.jpg"},
    "D3": {"nom": "Vanne D3", "lat": 43.424306, "lon": 3.095139, "parcelles_associées": ["arraché"], "ha": 0, "borne_associée": "B_D"},
    "D4": {"nom": "Vanne D4", "lat": 43.424306, "lon": 3.095139, "parcelles_associées": ["Phylloxera"], "ha": 2.12, "borne_associée": "B_D"},
    "D5": {"nom": "Vanne D5", "lat": 43.422917, "lon": 3.095611, "parcelles_associées": ["Vio source Ro"], "ha": 0.59, "borne_associée": "B_D"},
    "D6": {"nom": "Vanne D6", "lat": 43.421417, "lon": 3.095222, "parcelles_associées": ["Syrah Coural"], "ha": 0.79, "borne_associée": "B_D", "photo": "pages/images/vannes_azalet.jpg"},
    "D7": {"nom": "Vanne D7", "lat": 43.424972, "lon": 3.093083, "parcelles_associées": ["?"], "ha": 0, "borne_associée": "B_D"},
    "D8": {"nom": "Vanne D8", "lat": 43.427250, "lon": 3.093722, "parcelles_associées": ["Vio Jardin"], "ha": 0.86, "borne_associée": "B_D"},
    "D9": {"nom": "Vanne D9", "lat": 43.422917, "lon": 3.095611, "parcelles_associées": ["Alba coural pe"], "ha": 0.12, "borne_associée": "B_D"},
    "D10": {"nom": "Vanne D10", "lat": 43.421194, "lon": 3.097028, "parcelles_associées": ["Alba Coural"], "ha": 0.9, "borne_associée": "B_D"},
    "D11": {"nom": "Vanne D11", "lat": 43.421417, "lon": 3.095222, "parcelles_associées": ["viognier Alazet"], "ha": 0.8, "borne_associée": "B_D"},
    "D12": {"nom": "Vanne D12", "lat": 43.421417, "lon": 3.095222, "parcelles_associées": ["viognier Alazet"], "ha": 0.43, "borne_associée": "B_D"},
    "D13": {"nom": "Vanne D13", "lat": 43.421417, "lon": 3.095222, "parcelles_associées": ["viognier Alazet"], "ha": 0.43, "borne_associée": "B_D"},
    "D14": {"nom": "Vanne D14", "lat": 43.421417, "lon": 3.095222, "parcelles_associées": ["viognier Alazet"], "ha": 0.43, "borne_associée": "B_D"},
    "D15": {"nom": "Vanne D15", "lat": 43.421417, "lon": 3.095222, "parcelles_associées": ["merlot"], "ha": 0.75, "borne_associée": "B_D"},

    "K1": {"nom": "Vanne K1", "lat": 43.423528, "lon": 3.085806, "parcelles_associées": ["petit bardou"], "ha": 1.0, "borne_associée": "B_K"},
    "K2": {"nom": "Vanne K2", "lat": 43.423528, "lon": 3.085806, "parcelles_associées": ["petit bardou"], "ha": 0.95, "borne_associée": "B_K"},
    "K3": {"nom": "Vanne K3", "lat": 43.423417, "lon": 3.087389, "parcelles_associées": ["Grand Bardou"], "ha": 1.0, "borne_associée": "B_K"},
    "K4": {"nom": "Vanne K4", "lat": 43.423417, "lon": 3.087389, "parcelles_associées": ["Grand Bardou"], "ha": 1.0, "borne_associée": "B_K"},
    "K5": {"nom": "Vanne K5", "lat": 43.423250, "lon": 3.088722, "parcelles_associées": ["Grand Bardou"], "ha": 1.0, "borne_associée": "B_K"},
    "K6": {"nom": "Vanne K6", "lat": 43.423250, "lon": 3.088722, "parcelles_associées": ["Grand Bardou"], "ha": 1.0, "borne_associée": "B_K"},
    "K7": {"nom": "Vanne K7", "lat": 43.423278, "lon": 3.089944, "parcelles_associées": ["Grand Bardou"], "ha": 1.0, "borne_associée": "B_K"},
    "K8": {"nom": "Vanne K8", "lat": 43.423278, "lon": 3.089944, "parcelles_associées": ["Grand Bardou"], "ha": 1.0, "borne_associée": "B_K"},
    "K9": {"nom": "Vanne K9", "lat": 43.423611, "lon": 3.091444, "parcelles_associées": ["?"], "ha": 0, "borne_associée": "B_K"},
    "K10": {"nom": "Vanne K10", "lat": 43.423611, "lon": 3.091444, "parcelles_associées": ["Plantier terret"], "ha": 1.0, "borne_associée": "B_K"},
    "K11": {"nom": "Vanne K11", "lat": 43.423611, "lon": 3.091444, "parcelles_associées": ["Plantier terret"], "ha": 1.12, "borne_associée": "B_K"},
    "K12": {"nom": "Vanne K12", "lat": 43.421583, "lon": 3.089778, "parcelles_associées": ["Brunaude Alba"], "ha": 1.09, "borne_associée": "B_K"},
    "K13": {"nom": "Vanne K13", "lat": 43.421583, "lon": 3.089778, "parcelles_associées": ["La Brunaude"], "ha": 0.83, "borne_associée": "B_K"},
    "K14": {"nom": "Vanne K14", "lat": 43.421583, "lon": 3.089778, "parcelles_associées": ["Plantier Vio Br"], "ha": 0.75, "borne_associée": "B_K"},
    "K15": {"nom": "Vanne K15", "lat": 43.421583, "lon": 3.089778, "parcelles_associées": ["x"], "ha": 0, "borne_associée": "B_K"},
    "K16": {"nom": "Vanne K16", "lat": 43.421583, "lon": 3.089778, "parcelles_associées": ["CF Brunaude"], "ha": 0.69, "borne_associée": "B_K"}
}

# ====================== 2. FONCTIONS UTILITAIRES ======================

def get_image_html(image_path):
    """Transforme une image locale en code lisible par la carte"""
    # On vérifie si l'image est bien là
    if not os.path.exists(image_path):
        return f'<p style="color:red;"><b>ATTENTION:</b> Impossible de trouver l\'image : <i>{image_path}</i></p>'
        
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f'<img src="data:image/jpeg;base64,{encoded_string}" style="max-width:300px; width:100%; border-radius:5px; margin-bottom:10px;">'
    except Exception as e:
        return f"<p style='color:red;'><i>Erreur technique avec l'image: {e}</i></p>"
    
def create_popup_content(equipement, equipement_type):
    if equipement_type == "borne":
        # Gestion de la photo de la borne si elle existe
        photo_html = ""
        if "photo" in equipement:
            photo_html = get_image_html(equipement["photo"])
            
        return f"""
        {photo_html}
        <h4>{equipement['nom']}</h4>
        <b>Débit:</b> {equipement['debit']} m³/h<br>
        <b>Pression:</b> {equipement['pression']} bars<br>
        <b>Surface couverte:</b> {equipement['hectares']} ha<br>
        <hr>
        {equipement.get('explications', '')}
        """
        
    elif equipement_type == "vannes_groupees":
        # On cherche si au moins une des vannes du groupe a une photo
        photo_html = ""
        for v in equipement:
            if "photo" in v:
                photo_html = get_image_html(v["photo"])
                break # On s'arrête à la première photo trouvée pour ce groupe
                
        html = f"{photo_html}<h4>📍 Regroupement de {len(equipement)} vanne(s)</h4>"
        for v in equipement:
            parcelles_str = ", ".join(v['parcelles_associées'])
            html += f"<b>{v['nom']}</b> (Reliée à {v['borne_associée']})<br>"
            html += f"🌱 Parcelle(s): {parcelles_str}<br>"
            html += f"📏 Surface: {v.get('ha', 0)} ha<br>"
            html += "<hr style='margin: 5px 0;'>"
        return html
        
    return ""

def add_parcelle_to_map(m, parcelle_id, parcelle):
    """Ajoute une parcelle à la carte Folium"""
    color_map = {
        "Syrah": "#8B0000", "Viognier": "#FFD700", "Grenache": "#FF6347",
        "Chardonnay": "#F5DEB3", "Albarino": "#90EE90", "Merlot": "#800020",
        "Cinsault": "#FFB6C1", "Marselan": "#800080"
    }

    folium.GeoJson(
        parcelle["geometry"],
        style_function=lambda x: {
            "fillColor": color_map.get(parcelle["cepage"], "#3388ff"),
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.5
        },
        tooltip=f"{parcelle['nom']} ({parcelle['cepage']}) - {parcelle['surface']} ha"
    ).add_to(m)

# ====================== 3. CRÉATION DE LA CARTE ======================
# Calcul du centre en utilisant 'coords' pour les BORNES
center_lat = sum(b["coords"][0] for b in DATA_BORNES.values()) / len(DATA_BORNES)
center_lon = sum(b["coords"][1] for b in DATA_BORNES.values()) / len(DATA_BORNES)

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=15,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr='Tiles &copy; Esri'
)

# --- 1. Ajouter les PARCELLES ---
for parcelle_id, parcelle in DATA_PARCELLES.items():
    add_parcelle_to_map(m, parcelle_id, parcelle)

# --- 2. Ajouter les BORNES (CORRIGÉ avec coords[0] et coords[1]) ---
for borne_id, borne in DATA_BORNES.items():
    popup_content = create_popup_content(borne, "borne")
    folium.Marker(
        location=[borne["coords"][0], borne["coords"][1]], 
        icon=folium.Icon(color="blue", icon="tint", prefix="fa"),
        tooltip=f"Borne {borne_id}"
    ).add_child(folium.Popup(popup_content, max_width=300)).add_to(m)

# --- 3. Ajouter les VANNES ---
# --- 3. Ajouter les VANNES (Regroupées par coordonnées) ---
vannes_par_coords = {}

# On trie les vannes selon leurs coordonnées GPS
for vanne_id, vanne in DATA_VANNES.items():
    coords = (vanne["lat"], vanne["lon"])
    if coords not in vannes_par_coords:
        vannes_par_coords[coords] = []
    vannes_par_coords[coords].append(vanne)

# On affiche un seul marqueur par groupe de coordonnées
for coords, liste_vannes in vannes_par_coords.items():
    popup_content = create_popup_content(liste_vannes, "vannes_groupees")
    
    # Le texte au survol de la souris
    noms_vannes = ", ".join([v["nom"] for v in liste_vannes])
    tooltip_text = f"{len(liste_vannes)} Vanne(s) : {noms_vannes}"
    
    folium.Marker(
        location=[coords[0], coords[1]],
        icon=folium.Icon(color="green", icon="fa-faucet", prefix="fa"),
        tooltip=tooltip_text
    ).add_child(folium.Popup(popup_content, max_width=350)).add_to(m)


# --- 4. Relier bornes et vannes (CORRIGÉ avec coords[0] et coords[1]) ---
for borne_id, borne in DATA_BORNES.items():
    for vanne_id in borne.get("vannes_associées", []):
        if vanne_id in DATA_VANNES:
            folium.PolyLine(
                locations=[
                    [borne["coords"][0], borne["coords"][1]],
                    [DATA_VANNES[vanne_id]["lat"], DATA_VANNES[vanne_id]["lon"]]
                ],
                color="blue",
                weight=2,
                dash_array="5,5"
            ).add_to(m)

# ====================== 4. AFFICHAGE ======================
st.title("💧 Gestion de l'Irrigation")
st_folium(m, width=1200, height=800, returned_objects=[])
