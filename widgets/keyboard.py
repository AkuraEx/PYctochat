from tkinter import Button, Frame, Misc

from app import Separator


class Keyboard(Frame):
    def __init__(self, master: Misc | None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        keys = Frame(self, background="black")
        button_container = Frame(self)

        send = Button(self, text="Send")
        save = Button(self, text="Save")
        delete = Button(self, text="Delete?")

        keys.pack(side="left", expand=True, fill="both")
        Separator(self, orient="vertical").pack(fill="y", expand=True)
        send.pack()
        save.pack()
        delete.pack()
