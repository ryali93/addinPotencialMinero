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
            from tkinter import *
            import tkMessageBox
            from PIL import ImageTk, Image
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
            self._dlg = ventanaLogin()
        return self._dlg

    def onClick(self):
        """Show the rename data frame dialog."""
        try:
            self.dlg.Show(True)
            self.dlg.Centre(True)
        except Exception as e:
            pythonaddins.MessageBox(e.message, msg.error, 0)

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

class ventanaLogin(object):
    """docstring for ventanaLogin"""
    def __init__(self):
        self.window = Tk()
        self.window.title("Iniciar Sesion")
        self.window.geometry('370x200')
        self.window.iconbitmap(os.path.join(os.path.dirname(__file__), "student_min.ico"))
        self.window.attributes("-alpha", 0.95)

        img = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__), "student_medium.png")))
        panel = Label(self.window, image = img)
        panel.grid(column=0, row=0)

        img2 = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__), "ingemmet_logo.png")))
        panel2 = Label(self.window, image = img2)
        panel2.grid(column=1, row=0)

        lbl = Label(self.window, text="Usuario:")
        lbl.grid(column=0, row=1)
        self.usuarioInput = Entry(self.window, width=45)
        self.usuarioInput.grid(column=1, row=1)

        lbl2 = Label(self.window, text="Password:")
        lbl2.grid(column=0, row=2, pady=5)
        self.contrasenaInput = Entry(self.window, width=45)
        self.contrasenaInput.config(show="*");
        self.contrasenaInput.grid(column=1, row=2, pady=5   )

        btn = Button(self.window, text="Login", width=48, relief='raised', command=self.OnOK)
        btn.grid_columnconfigure(0, weight=3)
        btn.grid(column=0, columnspan=3, row=4, padx=10, pady=10)
        self.window.mainloop()

    def OnOK(self):
        usuario_default = "admin"
        clave_default = "123456"
        if self.usuarioInput.get() == usuario_default and self.contrasenaInput.get() == clave_default:
            tkMessageBox.showinfo('Bienvenido', 'Info')
            addin_addin.login.enabled = False
            addin_addin.potencialMinero.enabled = True
            addin_addin.workspace.enabled = True
            addin_addin.controlador.controller = 1
            self.window.quit()
        else:
            tkMessageBox.showinfo('Error', 'El usuario o el password ingresado no es el correcto')