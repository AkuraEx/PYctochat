from tkinter import Button, Frame, Label, Misc, PhotoImage
from app import Separator
import config as C

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import PictoChatApp


class Tools(Frame):
    def __init__(
        self, master: Misc | None, app: "PictoChatApp", *args, **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        self.icons: dict[str, PhotoImage] = {}
        self.icons["clear"] = PhotoImage(file="assets/pictochatlogo.png")
        self.icons["quit"] = PhotoImage(file="assets/close.png")
        self.icons["pencil"] = PhotoImage(file="assets/pencil.png")
        self.icons["eraser"] = PhotoImage(file="assets/eraser.png")
        self.icons["more"] = PhotoImage(file="assets/more.png")
        self.icons["less"] = PhotoImage(file="assets/less.png")
        self.icons["undo"] = PhotoImage(file="assets/undo.png")

        clear = Button(
            self, text="Clear", command=app.clear, image=self.icons["clear"]
        )

        quit = Button(
            self, text="Quit", command=app.quit, image=self.icons["quit"]
        )

        save = Button(self, text="Save", command=app.save)

        undo = Button(
            self, text="Undo", command=app.undo, image=self.icons["undo"]
        )

        pencil = Button(
            self, text="Pencil", command=app.pencil, image=self.icons["pencil"]
        )

        eraser = Button(
            self, text="Eraser", command=app.eraser, image=self.icons["eraser"]
        )

        more = Button(
            self, text="More", command=app.more, image=self.icons["more"]
        )
        less = Button(
            self, text="Less", command=app.less, image=self.icons["less"]
        )

        quit.pack()
        Separator(self, orient="horizontal").pack(fill="x", expand=True)
        undo.pack()
        save.pack(fill="x")
        Separator(self, orient="horizontal").pack(fill="x", expand=True)
        pencil.pack()
        eraser.pack()
        Separator(self, orient="horizontal").pack(fill="x", expand=True)
        more.pack()
        less.pack()
        Separator(self, orient="horizontal").pack(fill="x", expand=True)
        clear.pack()
