import sys

sys.path.insert(0, r'\\srvfs01\bdgeocientifica$\Addins_Geoprocesos\PotencialMinero\pminerodev')

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


# Potencial Minero Metalico

class pmmUnidadesGeologicas(object):
    """Implementation for addinProject_addin.pmmUnidadesGeologicas (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T02'])


class pmmFallasGeologicas(object):
    """Implementation for addinProject_addin.pmmFallasGeologicas (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T03'])


class pmmDepositosMinerales(object):
    """Implementation for addinProject_addin.pmmDepositosMinerales (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T04'])


class pmmGeoquimica(object):
    """Implementation for addinProject_addin.pmmGeoquimica (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T05'])


class pmmSensoresRemotos(object):
    """Implementation for addinProject_addin.pmmSensoresRemotos (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T06'])


class PotencialMineroMetalico(object):
    """Implementation for addinProject_addin.PotencialMineroMetalico (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T07'])


# Potencial Minero No Metalico

class rmiLitologia(object):
    """Implementation for addinProject_addin.rmiLitologia (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T08'])


class rmiSustancias(object):
    """Implementation for addinProject_addin.rmiSustancias (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T09'])


class rmiConcesiones(object):
    """Implementation for addinProject_addin.rmiConcesiones (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T10'])


class rmiSensoresRemotos(object):
    """Implementation for addinProject_addin.rmiSensoresRemotos (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T11'])


class rmiAccesos(object):
    """Implementation for addinProject_addin.rmiAccesos (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T12'])


class PotencialMineroNoMetalico(object):
    """Implementation for addinProject_addin.PotencialMineroNoMetalico (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T13'])


class crearDirectorioTrabajo(object):
    """Implementation for addinProject_addin.workspace (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, TOOL_NAME['T01'])


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
