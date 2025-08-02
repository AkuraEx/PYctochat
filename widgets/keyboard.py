from tkinter import Button, Frame, Misc
from tkinter.ttk import Separator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import PictoChatApp
BTN_PADDING = 4


class Keyboard(Frame):
    def __init__(
        self, master: Misc | None, app: "PictoChatApp", *args, **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        keys = Frame(self, background="white")
        button_container = Frame(self)

        send = Button(button_container, text="Send", command=app.send)
        save = Button(button_container, text="Save")
        delete = Button(button_container, text="Delete?")

        send.pack(fill="both", expand=True, padx=BTN_PADDING, pady=BTN_PADDING)
        save.pack(fill="both", expand=True, padx=BTN_PADDING, pady=BTN_PADDING)
        delete.pack(
            fill="both", expand=True, padx=BTN_PADDING, pady=BTN_PADDING
        )

        keys.pack(side="left", expand=True, fill="both")
        button_container.pack(side="right", fill="y", expand=False)
        Separator(self, orient="vertical").pack(side="right", fill="y")
