import os
import arcpy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC = os.path.join(BASE_DIR, 'statics')
TMP_GDB = arcpy.env.scratchGDB

CONN = os.path.join(STATIC, 'conn\\bdgeocat_publ_gis.sde')

GDB_TEMPLATE = os.path.join(STATIC, 'gdb')
TBX = os.path.join(STATIC, 'tbx\\PotencialMinero.tbx')
TOOL_NAME = {
    'T01': 'EstructuraDirectorio',
    'T02': 'unidadesGeologicas',
    'T03': 'fallasGeologicas',
    'T04': 'depositosMinerales',
    'T05': 'geoquimica',
    'T06': 'sensoresRemotos',
    'T07': 'PotencialMinero',
}
USER_GUIDE = os.path.join(STATIC, 'potencial-minero-user-guide.pdf')

NAME_GDB = 'DRME_PM.gdb'