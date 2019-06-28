import os
import wx
import addin_addin

class ventanaLogin(wx.Frame):

    def __init__(self):
        """Initialize the Frame and add wx widgets."""
        wx.Frame.__init__(self, parent=None, title="Iniciar Sesion", style=wx.CAPTION | wx.MINIMIZE_BOX |wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CLIP_CHILDREN, size=(380, 240))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.DEFAULT_ALPHA = 240
        self.SetTransparent(self.DEFAULT_ALPHA)

        icon = wx.Icon(os.path.join(os.path.dirname(__file__), "student_min.ico"), wx.BITMAP_TYPE_ICO, 16, 16)
        self.SetIcon(icon)

        self.panelimage = wx.Panel(self)
        self.panel01 = wx.Panel(self)
        self.panel02 = wx.Panel(self)
        self.panel03 = wx.Panel(self)

        pic = wx.StaticBitmap(self.panelimage)
        pic.SetBitmap(wx.Bitmap(os.path.join(os.path.dirname(__file__), "student_medium.png")))
        logoingemmet = wx.StaticBitmap(self.panelimage)
        logoingemmet.SetBitmap(wx.Bitmap(os.path.join(os.path.dirname(__file__), "ingemmet_logo.png")))

        sz = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sz)

        sz.Add(self.panelimage, 3, wx.EXPAND|wx.ALL, 0)
        sz.Add(self.panel01, 1, wx.EXPAND|wx.ALL, 0)
        sz.Add(self.panel02, 1, wx.EXPAND|wx.ALL, 0)
        sz.Add(self.panel03, 1, wx.EXPAND|wx.ALL, 0)

        szpanelimage = wx.BoxSizer(wx.HORIZONTAL)
        self.panelimage.SetSizer(szpanelimage)

        szpanel01 = wx.BoxSizer(wx.HORIZONTAL)
        self.panel01.SetSizer(szpanel01)

        szpanel02 = wx.BoxSizer(wx.HORIZONTAL)
        self.panel02.SetSizer(szpanel02)

        szpanel03 = wx.BoxSizer(wx.HORIZONTAL)
        self.panel03.SetSizer(szpanel03)

        usuario = wx.StaticText(self.panel01, -1, "Usuario:")
        self.usuarioInput = wx.TextCtrl(self.panel01, -1, style=wx.TE_PROCESS_ENTER) 
        clave = wx.StaticText(self.panel02, -1, "Password:")
        self.claveInput = wx.TextCtrl(self.panel02, -1, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        botonValidar = wx.Button(self.panel03, label="Login")


        szpanelimage.Add(pic, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 4)
        szpanelimage.Add(logoingemmet, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 4)
        szpanel01.Add(usuario, 1,  wx.ALIGN_CENTER_VERTICAL|wx.ALL, 4)
        szpanel01.Add(self.usuarioInput, 3, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 4)
        szpanel02.Add(clave, 1,  wx.ALIGN_CENTER_VERTICAL|wx.ALL, 4)
        szpanel02.Add(self.claveInput, 3, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 4)
        szpanel03.Add(botonValidar, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 4)

        self.Bind(wx.EVT_BUTTON, self.OnOK)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnOK)


    def OnClose(self, event):
        """Close the frame. Do not use destroy."""
        self.Show(False)
    # End OnClose event method

    def OnOK(self, event):
        """Renames the active data frame of map document."""
        usuario_default = "admin"
        clave_default = "123456"
        if self.usuarioInput.GetValue() == usuario_default and self.claveInput.GetValue() == clave_default:
            wx.MessageBox('Bienvenido', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.Show(False)
            addin_addin.login.enabled = False
            addin_addin.potencialMinero.enabled = True
            addin_addin.workspace.enabled = True
            addin_addin.controlador.controller = 1
        else:
            wx.MessageBox('El usuario o el password ingresado no es el correcto', 'Error', wx.OK | wx.ICON_HAND)
