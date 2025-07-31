from tkinter.ttk import Separator
import pygame
import os
from tkinter import Frame, Tk
import config as C
from canvas import PolygonCanvas
from widgets.chat import Chat
from widgets.embed import Embed
from widgets.tools import Tools
from widgets.keyboard import Keyboard


class PictoChatApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("PictoChat P2P")
        self.root.geometry(C.GEOMETRY)

        self.embed = Embed(root, width=C.SCREEN_WIDTH, height=C.SCREEN_HEIGHT)

        os.environ["SDL_WINDOWID"] = str(self.embed.winfo_id())

        self.running = True

        self.tools = Tools(root, self)
        self.chat = Chat(root)
        self.keyboard = Keyboard(root)

        self.tools.pack(side="left", fill="y", expand=False, padx=10, pady=10)
        self.embed.pack(side="top", anchor="nw")
        self.keyboard.pack(side="bottom", anchor="sw")
        self.chat.pack(side="right", fill="y")

        self.embed.update()

        # self.canvas = PolygonCanvas(C.CANVAS, C.BLACK, C.WHITE, C.LINE_THICKNESS)

        self.root.after(10, self.pygame_loop)

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
        self.canvas.undo()

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
