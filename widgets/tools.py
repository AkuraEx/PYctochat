from tkinter import Button, Frame, Misc, PhotoImage

from tkinter.ttk import Separator
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from app import PictoChatApp


class Tools(Frame):
    def __init__(
        self, master: Misc | None, app: "PictoChatApp", *args, **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        #  Load icons
        self.icons: dict[str, PhotoImage] = {}
        self.icons["clear"] = PhotoImage(file="assets/pictochatlogo.png")
        self.icons["quit"] = PhotoImage(file="assets/close.png")
        self.icons["pencil"] = PhotoImage(file="assets/pencil.png")
        self.icons["eraser"] = PhotoImage(file="assets/eraser.png")
        self.icons["red"] = PhotoImage(file="assets/red.png")
        self.icons["green"] = PhotoImage(file="assets/green.png")
        self.icons["blue"] = PhotoImage(file="assets/blue.png")
        self.icons["more"] = PhotoImage(file="assets/more.png")
        self.icons["less"] = PhotoImage(file="assets/less.png")
        self.icons["undo"] = PhotoImage(file="assets/undo.png")

        # Register buttons
        clear = self._register_button("Clear", app.clear, "clear")
        quit = self._register_button("Quit", app.quit, "quit")
        undo = self._register_button("Undo", app.undo, "undo")
        pencil = self._register_button("Pencil", app.pencil, "pencil")
        eraser = self._register_button("Eraser", app.eraser, "eraser")
        red = self._register_button("Red", app.red, "red")
        green = self._register_button("Green", app.green, "green")
        blue = self._register_button("Blue", app.blue, "blue")
        more = self._register_button("More", app.more, "more")
        less = self._register_button("Less", app.less, "less")

        # Pack them
        quit.pack()
        Separator(self, orient="horizontal").pack(fill="x", expand=True)
        undo.pack()
        Separator(self, orient="horizontal").pack(fill="x", expand=True)
        pencil.pack()
        eraser.pack()
        Separator(self, orient="horizontal").pack(fill="x", expand=True)
        red.pack()
        green.pack()
        blue.pack()
        more.pack()
        less.pack()
        Separator(self, orient="horizontal").pack(fill="x", expand=True)
        clear.pack()

    def _register_button(
        self,
        text: str,
        command: Callable[[], None],
        image_name: str | None = None,
    ) -> Button:
        if image_name:
            return Button(
                self,
                text=text,
                command=command,
                image=self.icons[image_name],
            )
        return Button(
            self,
            text=text,
            command=command,
        )
