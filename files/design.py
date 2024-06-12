import tkinter as tk
from tkinter import font
from config import GRAY, ONYX, BLUSH, NON_BLUE, ROBIN_BLUE

import utils.screen_center as sc
import utils.read_image as ri


class Design(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logo = ri.leer_imagen("./utils/logo.png", (100, 100))
        # self.perfil = assets.resize_image(assets.PERFIL, (100, 100))
        font.families()
        self.config_window()
        self.paneles()
        self.controls()
        self.controls_lateral()

    def config_window(self):
        self.title("Finger Print Tcontur ")
        self.iconbitmap("./utils/favicon.ico")
        w, h = 1024, 600
        sc.screen_center(self, w, h)

    def paneles(self):
        self.barra_superior = tk.Frame(self, bg=ONYX, height=150)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=GRAY, width=300, )
        self.menu_lateral.pack(side=tk.LEFT, fill='both', )

        self.contenido = tk.Frame(self, bg=BLUSH, width=150)  # width= no es necesario ya que se expande
        self.contenido.pack(side=tk.RIGHT, fill='both', expand=True)

    def controls(self):
        font_awesome = font.Font(family='FontAwesome', size=12)
        self.label_title = tk.Label(self.barra_superior, text="Finger Print Tcontur")
        self.label_title.config(fg="#fff",
                                bg=ONYX,
                                font=("Roboto", 15),
                                pady=10,
                                width=16)
        self.label_title.pack(side=tk.LEFT)

        # Btn del menu lateral
        # self.btn_home = tk.Button(self.barra_superior,
        #                           text="\uf0c9",
        #                           font=font_awesome,
        #                           bd=0,
        #                           bg=ONYX,
        #                           fg="white")
        # self.btn_home.pack(side=tk.LEFT)

        # etiqueta de informacion
        self.label_info = tk.Label(self.barra_superior, text="tcontur@tcontur.com")
        self.label_info.config(fg="#fff",
                               bg=ONYX,
                               font=("Roboto", 10),
                               padx=10,
                               width=20)
        self.label_info.pack(side=tk.RIGHT)

    def controls_lateral(self):
        with_menu = 20
        height_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=8)
        self.labelPerfil = tk.Label(self.menu_lateral, image=self.logo, bg=GRAY)
        self.labelPerfil.pack(side=tk.TOP, pady=10, )

        self.buttonDashboard = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)
        self.buttonSettings = tk.Button(self.menu_lateral)

        buttons_config = [
            (self.buttonDashboard, "\uf200", "Dashboard"),
            (self.buttonInfo, "\uf05a", "Info"),
            (self.buttonSettings, "\uf013", "Settings")
        ]

        for button, icon, text in buttons_config:
            self.config_buttons(button, icon, text, font_awesome, with_menu, height_menu)

    def config_buttons(self, button, icon, text, font_awesome, with_menu, height_menu):
        button.config(text=icon + " " + text,
                      font=font_awesome,
                      bd=0,
                      bg=GRAY,
                      fg="white",
                      width=with_menu,
                      height=height_menu)
        button.pack(side=tk.TOP, )
