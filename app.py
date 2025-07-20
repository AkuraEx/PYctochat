import pygame
import os
from tkinter import Frame, Tk, PhotoImage, Button
import config as C
from canvas import PolygonCanvas


class PictoChatApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("PictoChat P2P")
        self.root.geometry("576x576")

        self.embed = Frame(root, width=C.WINDOW_WIDTH, height=C.WINDOW_HEIGHT)
        self.embed.pack()
        self.embed.update()

        os.environ["SDL_WINDOWID"] = str(self.embed.winfo_id())

        self.running = True

        self._create_tools()

        self.canvas = PolygonCanvas(
            C.CANVAS, C.BLACK, C.WHITE, C.LINE_THICKNESS
        )

        self.root.after(10, self.pygame_loop)

    def _load_assets(self):
        self.icons: dict[str, PhotoImage] = {}
        self.icons["clear"] = PhotoImage(file="assets/pictochatlogo.png")
        self.icons["quit"] = PhotoImage(file="assets/close.png")
        self.icons["pencil"] = PhotoImage(file="assets/pencil.png")
        self.icons["eraser"] = PhotoImage(file="assets/eraser.png")
        self.icons["more"] = PhotoImage(file="assets/more.png")
        self.icons["less"] = PhotoImage(file="assets/less.png")
        self.icons["undo"] = PhotoImage(file="assets/undo.png")

    def _create_tools(self):
        self._load_assets()

        self.tools = Frame(self.root, bg="white")
        self.tools.place(x=0, y=0, width=100, height=C.WINDOW_HEIGHT)

        Button(
            self.tools,
            text="Clear",
            command=self.clear,
            image=self.icons["clear"],
        ).place(x=5, y=480)

        Button(
            self.tools,
            text="Quit",
            command=self.quit,
            image=self.icons["quit"],
        ).place(x=5, y=0)

        Button(
            self.tools,
            text="Save",
            command=self.save,
        ).place(x=5, y=60)

        Button(
            self.tools,
            text="Undo",
            command=self.undo,
            image=self.icons["undo"],
        ).place(x=5, y=60)

        Button(
            self.tools,
            text="Pencil",
            command=self.pencil,
            image=self.icons["pencil"],
        ).place(x=5, y=300)

        Button(
            self.tools,
            text="Eraser",
            command=self.eraser,
            image=self.icons["eraser"],
        ).place(x=5, y=340)

        Button(
            self.tools,
            text="More",
            command=self.more,
            image=self.icons["more"],
        ).place(x=5, y=400)

        Button(
            self.tools,
            text="Less",
            command=self.less,
            image=self.icons["less"],
        ).place(x=5, y=440)

    def clear(self):
        self.canvas.clear()

    def quit(self):
        self.running = False
        pygame.quit()
        self.root.destroy()

    def save(self):
        # TODO: Something with self.canvas.bytes()
        pass

    def undo(self):
        self.canvas._undo()

    def pencil(self):
        self.canvas.color = C.BLACK

    def eraser(self):
        self.canvas.color = C.WHITE

    def more(self):
        self.canvas.thickness = C.LINE_THICKNESS + 5

    def less(self):
        self.canvas.thickness = C.LINE_THICKNESS

    def pygame_loop(self):
        if not self.running:
            return
        self.canvas.do_frame()
        self.root.after(10, self.pygame_loop)
