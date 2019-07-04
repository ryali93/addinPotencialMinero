import pythonaddins
import threading
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dev"))
from config import *
from messages import Messages
import webbrowser

msg = Messages

def controlador():
    f = open("dev/sesion.txt", "r")
    value = f.read()
    f.close()
    return(int(value))

class extensionIniciarSesion(object):
    """Implementation for addin_addin.wxpyextension (Extension)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

        f = open("dev/sesion.txt", "w")
        f.write("0")
        f.close()

class iniciarSesion(object):
    """Implementation for addin_addin.login (Button)"""
    def __init__(self):
        """Initialize button and set it to enabled and unchecked by default."""
        self.enabled = True
        self.checked = False

class crearDirectorioTrabajo(object):
    """Implementation for addin_addin.workspace (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "EstructuraDirectorio")

class PMM_V1_unidadesGeologicas(object):
    """Implementation for addin_addin.PMM_V1_unidadesGeologicas (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMunidadesGeologicas")

class PMM_V3_fallasGeologicas(object):
    """Implementation for addin_addin.PMM_V3_fallasGeologicas (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMfallasGeologicas")

class PMM_V4_depositosMinerales(object):
    """Implementation for addin_addin.PMM_V4_depositosMinerales (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMdepositosMinerales")

class PMM_V5_geoquimica(object):
    """Implementation for addin_addin.PMM_V5_geoquimica (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMgeoquimica")

class PMM_V6_SensoresRemotos(object):
    """Implementation for addin_addin.PMM_V6_SensoresRemotos (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMsensoresRemotos")

class potencialMineroMetalico(object):
    """Implementation for addin_addin.potencialMineroMetalico (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMPotencialMinero")

class RMI_V1_litologia(object):
    """Implementation for addin_addin.RMI_V1_litologia (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class RMI_V2_sustancias(object):
    """Implementation for addin_addin.RMI_V2_sustancias (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class RMI_V4_SensoresRemotos(object):
    """Implementation for addin_addin.RMI_V4_SensoresRemotos (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class RMI_V5_accesos(object):
    """Implementation for addin_addin.RMI_V5_accesos (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class potencialMineroNoMetalico(object):
    """Implementation for addin_addin.potencialMineroNoMetalico (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

def OpenBrowserURL():
    url = 'http://www.ingemmet.gob.pe/'
    webbrowser.open(url,new=0)

class abrirUrl(object):
    """Implementation for addin_addin.url (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        t = threading.Thread(target=OpenBrowserURL)
        t.start()
        t.join()
