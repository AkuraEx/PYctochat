from tkinter import Button, Frame, Misc, PhotoImage
from typing import TYPE_CHECKING
from PIL import Image, ImageTk

if TYPE_CHECKING:
    from app import PictoChatApp
BTN_PADDING = 4


class Keyboard(Frame):
    def __init__(
        self, master: Misc | None, app: "PictoChatApp", *args, **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        keys = Frame(self)
        button_container = Frame(self)

        #  Load icons
        self.icons: dict[str, PhotoImage] = {}
        img_send = Image.open("assets/send.png")
        img_save = Image.open("assets/save.png")
        img_delete = Image.open("assets/delete.png")

        self.icons["send"] = ImageTk.PhotoImage(img_send)
        self.icons["save"] = ImageTk.PhotoImage(img_save)
        self.icons["delete"] = ImageTk.PhotoImage(img_delete)

        send = Button(
            button_container, command=app.send, image=self.icons["send"]
        )
        save = Button(
            button_container, command=app.save, image=self.icons["save"]
        )
        delete = Button(
            button_container, command=app.save, image=self.icons["delete"]
        )

        send.pack(padx=BTN_PADDING)
        save.pack(padx=BTN_PADDING)
        delete.pack(padx=BTN_PADDING)

        keys.pack(side="left", expand=True, fill="both")
        button_container.pack(side="right", fill="y", expand=False)
