import streamlit as st
import folium
from streamlit_folium import st_folium
import json

# --- DONNÉES DES PARCELLES (celles que tu as partagées) ---
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
        }# ... (le reste de tes données DATA_PARCELLES)


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
