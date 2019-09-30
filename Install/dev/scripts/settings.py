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

    'T02': 'pmmUnidadesGeologicas',
    'T03': 'pmmFallasGeologicas',
    'T04': 'pmmDepositosMinerales',
    'T05': 'pmmGeoquimica',
    'T06': 'pmmSensoresRemotos',
    'T07': 'PotencialMineroMetalico',

    'T08': 'rmiLitologia',
    'T09': 'rmiSustancias',
    'T10': 'rmiConcesiones',
    'T11': 'rmiSensoresRemotos',
    'T12': 'rmiAccesos',
    'T13': 'PotencialMineroNoMetalico',

    'T14': 'PotencialMinero'
}
USER_GUIDE = os.path.join(STATIC, 'potencial-minero-user-guide.pdf')

NAME_GDB = 'DRME_PM.gdb'
