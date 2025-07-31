from tkinter import NE, NW, Frame, Label, Misc


class Embed(Frame):
    def __init__(self, master: Misc | None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        BORDER = 8

        self.user_color = "#ff73b2"
        self.alt_color = "#fb0071"
        self.user_name = "DEEZ"

        self.configure(
            highlightbackground=self.alt_color, highlightthickness=BORDER
        )

        self.label = Label(
            self,
            text=self.user_name,
            background=self.user_color,
            foreground=self.alt_color,
            highlightbackground=self.alt_color,
            highlightthickness=BORDER,
            font=("Pixelify Sans", 32),
            padx=20,
            pady=4,
        )

        self.label.place(x=-BORDER, y=-BORDER, anchor=NW)
