from tkinter import Frame, Label, Misc

BORDER = 8


class Embed(Frame):
    def __init__(self, master: Misc | None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.user_color = "#ff73b2"
        self.alt_color = "#fb0071"
        self.user_name = "DEEZ"

        self.canvas_frame = Frame(
            self,
            width=self.canvas_width,
            height=self.canvas_height,
        )

        self.configure(
            highlightbackground=self.alt_color,
            highlightthickness=BORDER,
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

        self.canvas_frame.pack(anchor="center", fill="both", expand=True)
        self.label.place(x=-BORDER, y=-BORDER, anchor="nw")

    @property
    def canvas_width(self):
        return self.winfo_width() - (BORDER * 2)

    @property
    def canvas_height(self):
        return self.winfo_height() - (BORDER * 2)
