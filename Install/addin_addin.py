import arcpy
import pythonaddins
import threading
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dev"))
from config import *
import webbrowser
from messages import Messages
msg = Messages()

class controlador:
    def __init__(self):
        self.controller = 0

class extensionIniciarSesion(object):
    """Implementation for addin_addin.wxpyextension (Extension)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def startup(self):
        """On startup of ArcGIS, create the wxPython Simple app and start the mainloop."""
        try:
            from wx import App
            from wx import Locale
            from wx import LANGUAGE_ENGLISH
            self._wxApp = App()
            self._wxApp.locale = Locale(LANGUAGE_ENGLISH)
            self._wxApp.MainLoop()
        except Exception:
            pythonaddins.MessageBox("Error starting Rename Data Frame extension.", "Extension Error", 0)
    @property
    def enabled(self):
        """Enable or disable the RenameDataFrame button when the extension is turned on or off."""
        if self._enabled == False:
            login.enabled = False
        else:
            login.enabled = True
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """Set the enabled property of this extension when the extension is turned on or off in the Extension Dlalog of ArcMap."""
        self._enabled = value


class iniciarSesion(object):
    """Implementation for addin_addin.login (Button)"""
    _dlg = None

    def __init__(self):
        """Initialize button and set it to enabled and unchecked by default."""
        self.enabled = True
        self.checked = False

    @property
    def dlg(self):
        """Return the rename data frame dialog."""
        if self._dlg is None:
            from guiwx import ventanaLogin
            self._dlg = ventanaLogin()
        return self._dlg

    def onClick(self):
        """Show the rename data frame dialog."""
        try:
            self.dlg.Show(True)
            self.dlg.Centre(True)
        except Exception as e:
            pythonaddins.MessageBox(e.message, msg.error, 0)
            pass

class crearDirectorioTrabajo(object):
    """Implementation for addin_addin.workspace (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        try:
            if controlador.controller == 1:
                pythonaddins.GPToolDialog(TBX, "EstructuraDirectorio")
            else:
                pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        except:
            pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)


class PMM_V1_unidadesGeologicas(object):
    """Implementation for addin_addin.PMM_V1_unidadesGeologicas (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        try:
            if controlador.controller == 1:
                pythonaddins.GPToolDialog(TBX, "PMMunidadesGeologicas")
            else:
                pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        except:
            pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)

class PMM_V3_fallasGeologicas(object):
    """Implementation for addin_addin.PMM_V3_fallasGeologicas (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        try:
            if controlador.controller == 1:
                pythonaddins.GPToolDialog(TBX, "PMMfallasGeologicas")
            else:
                pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        except:
            pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)

class PMM_V4_depositosMinerales(object):
    """Implementation for addin_addin.PMM_V4_depositosMinerales (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        try:
            if controlador.controller == 1:
                pythonaddins.GPToolDialog(TBX, "PMMdepositosMinerales")
            else:
                pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        except:
            pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)

class PMM_V5_geoquimica(object):
    """Implementation for addin_addin.PMM_V5_geoquimica (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        try:
            if controlador.controller == 1:
                pythonaddins.GPToolDialog(TBX, "PMMgeoquimica")
            else:
                pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        except:
            pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)

class PMM_V6_SensoresRemotos(object):
    """Implementation for addin_addin.PMM_V6_SensoresRemotos (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        try:
            if controlador.controller == 1:
                pythonaddins.GPToolDialog(TBX, "PMMsensoresRemotos")
            else:
                pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        except:
            pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)

class potencialMinero(object):
    """Implementation for addin_addin.potencialMinero (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        try:
            if controlador.controller == 1:
                pythonaddins.GPToolDialog(TBX, "PMMPotencialMinero")
            else:
                pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)
        except:
            pythonaddins.MessageBox(msg.initsesion, msg.warning, 0)


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
