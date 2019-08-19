import sys

sys.path.insert(0, r'\\srvfs01\bdgeocientifica$\Addins_Geoprocesos\PotencialMinero\pminero')

import pythonaddins
import threading

from settings import *


class extensionIniciarSesion(object):
    pass


class iniciarSesion(object):
    """Implementation for addinProject_addin.login (Button)"""

    def __init__(self):
        self.enabled = False
        self.checked = False

    def onClick(self):
        pass


class V1_unidadesGeologicas(object):
    """Implementation for addinProject_addin.unidadesGeologicas (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T02'])


class V3_fallasGeologicas(object):
    """Implementation for addinProject_addin.fallasGeologicas (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T03'])


class V4_depositosMinerales(object):
    """Implementation for addinProject_addin.depositosMinerales (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T04'])


class V5_geoquimica(object):
    """Implementation for addinProject_addin.geoquimica (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T05'])


class V6_SesoresRemotos(object):
    """Implementation for addinProject_addin.sesoresRemotos (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T06'])


class crearDirectorioTrabajo(object):
    """Implementation for addinProject_addin.workspace (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T01'])


class potencialMinero(object):
    """Implementation for addinProject_addin.potencialMinero (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T07'])


def OpenBrowserURL():
    os.startfile(USER_GUIDE)


class abrirUrl(object):
    """Implementation for addinProject_addin.url (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        t = threading.Thread(target=OpenBrowserURL)
        t.start()
        t.join()
