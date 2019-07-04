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

    # @property
    # def enabled(self):
    #     """Enable or disable the RenameDataFrame button when the extension is turned on or off."""
    #     if self._enabled == False:
    #         login.enabled = False
    #     else:
    #         login.enabled = True
    #     return self._enabled
    #
    # @enabled.setter
    # def enabled(self, value):
    #     """Set the enabled property of this extension when the extension is turned on or off in the Extension Dlalog of ArcMap."""
    #     self._enabled = value

class iniciarSesion(object):
    """Implementation for addin_addin.login (Button)"""
    def __init__(self):
        """Initialize button and set it to enabled and unchecked by default."""
        self.enabled = True
        self.checked = False

    # def onClick(self):
    #     """Show the rename data frame dialog."""
    #     try:
    #         pythonaddins.MessageBox("Controlador", "Controlador", 0)
    #         pythonaddins.MessageBox(controlador(), "Controlador", 0)
    #         pythonaddins.MessageBox(type(controlador()), "Controlador", 0)
    #         if controlador() == 0:
    #             pythonaddins.MessageBox("GPToolDialog", "GPToolDialog", 0)
    #             pythonaddins.GPToolDialog(TBX, "InicioSesion")
    #     except Exception as e:
    #         pythonaddins.MessageBox(e.message, msg.error, 0)

class crearDirectorioTrabajo(object):
    """Implementation for addin_addin.workspace (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "EstructuraDirectorio")
        # try:
        #     if controlador() == 1:
        #         pass
        #     else:
        #         pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        # except:
        #     pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)


class PMM_V1_unidadesGeologicas(object):
    """Implementation for addin_addin.PMM_V1_unidadesGeologicas (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMunidadesGeologicas")
        # try:
        #     if controlador() == 1:
        #         pass
        #     else:
        #         pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        # except:
        #     pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)

class PMM_V3_fallasGeologicas(object):
    """Implementation for addin_addin.PMM_V3_fallasGeologicas (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMfallasGeologicas")
        # try:
        #     if controlador() == 1:
        #         pass
        #     else:
        #         pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        # except:
        #     pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)

class PMM_V4_depositosMinerales(object):
    """Implementation for addin_addin.PMM_V4_depositosMinerales (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMdepositosMinerales")
        # try:
        #     if controlador() == 1:
        #         pass
        #     else:
        #         pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        # except:
        #     pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)

class PMM_V5_geoquimica(object):
    """Implementation for addin_addin.PMM_V5_geoquimica (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMgeoquimica")
        # try:
        #     if controlador() == 1:
        #         pass
        #     else:
        #         pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        # except:
        #     pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)

class PMM_V6_SensoresRemotos(object):
    """Implementation for addin_addin.PMM_V6_SensoresRemotos (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMsensoresRemotos")
        # try:
        #     if controlador() == 1:
        #         pass
        #     else:
        #         pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        # except:
        #     pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)

class potencialMinero(object):
    """Implementation for addin_addin.potencialMinero (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, "PMMPotencialMinero")
        # try:
        #     if controlador() == 1:
        #         pass
        #     else:
        #         pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        # except:
        #     pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)


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
