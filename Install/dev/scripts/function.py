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
