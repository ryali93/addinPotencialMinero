from settings import *
import uuid


def path_database_input(zone):
    path = os.path.join(
        GDB_TEMPLATE, str(zone), NAME_GDB
    )
    return path


def name_folder(region):
    name = 'PM_%s_%s' % (region, uuid.uuid4().__str__())
    return name


def update_fields_accesos(input):
    with arcpy.da.UpdateCursor(input, ["NOMBRE", "RASGO_SECU", "TIPO"]) as cursor:
        for x in cursor:
            if len(x[0]) > 5:
                x[2] = "Asfaltada nacional"
            else:
                if x[1] == "Carretera Asfaltada":
                    x[2] = "Asfaltada local"
                elif x[1] == "Carretera Afirmada":
                    x[2] = "Afirmada"
                else:
                    x[2] = "Trocha"
            cursor.updateRow(x)
