from tkinter import *
import tkMessageBox
from PIL import ImageTk, Image
import os
# import addin_addin

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

    def app(self):
        self.window.mainloop()

ventanaLogin()