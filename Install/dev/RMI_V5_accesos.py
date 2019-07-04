import arcpy
from config import *

dataVias = os.path.join(CONN, 'DATA_GIS.DS_IGN_BASE_PERU_500000', 'DATA_GIS.IGN_TRA_VIAS')

buffer = {
    "8": "Asfaltada nacional",
    "4": "Asfaltada",
    "2": "Afirmada",
    "1": "Trocha",
    "0": "Sin via"
}

mql = arcpy.MakeQueryLayer_management(CONN, "mql", "SELECT * FROM {} WHERE {}".format(TBhasta, donde2))
arcpy.Clip_analysis(os.path.join(CONN, TBdesde), mql)


arcpy.Buffer_analysis(dataVias)

