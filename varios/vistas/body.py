import customtkinter as ctk


class Body(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        # self.pack(fill="both", expand=True)

        # pintar algo en el main frame
        # self.label = ctk.CTkLabel(self, text="Esta es la Vista Principal")
        # self.label.pack(padx=20, pady=20)
