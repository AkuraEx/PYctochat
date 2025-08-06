import pygame
import os
from tkinter import Label, Tk
import config as C
from PIL import Image, ImageTk
from canvas import PolygonCanvas
from canvas._base import BaseCanvas
import network
from widgets.chat import Chat
from widgets.embed import Embed
from widgets.tools import Tools
from widgets.keyboard import Keyboard

SCREEN_SIZE = {"width": C.SCREEN_WIDTH, "height": C.SCREEN_HEIGHT}
IMG_WIDTH = 234


class PictoChatApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("PictoChat P2P")
        self.root.resizable(False, False)

        self.root.rowconfigure(0, weight=1, minsize=C.SCREEN_HEIGHT)
        self.root.rowconfigure(1, weight=1, minsize=C.SCREEN_HEIGHT)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=8, minsize=C.SCREEN_WIDTH)
        self.root.columnconfigure(2, weight=4, minsize=C.CHAT_WIDTH)

        res = (root.winfo_screenwidth(), root.winfo_screenheight())

        bg_img = Image.open("assets/bg.png")
        self.bg_img = ImageTk.PhotoImage(bg_img.resize(res))  # type: ignore
        self.backdrop = Label(root, image=self.bg_img)

        self.embed = Embed(root, **SCREEN_SIZE)
        os.environ["SDL_WINDOWID"] = str(self.embed.canvas_frame.winfo_id())

        self.running = True
        self.connection = False

        self.keyboard = Keyboard(root, self, **SCREEN_SIZE)
        self.chat = Chat(root, width=C.CHAT_WIDTH)
        self.tools = Tools(root, self)

        self.tools.grid(
            sticky="ns", column=0, row=0, rowspan=2, padx=10, pady=10
        )
        self.embed.grid(sticky="nsew", column=1, row=0, pady=(10, 0))
        self.keyboard.grid(sticky="nsew", column=1, row=1, pady=(0, 10))
        self.chat.grid(sticky="s", column=2, row=0, rowspan=2, padx=10)
        self.backdrop.place(x=-5, y=-5)  # don't ask # I won't 

        self.root.bind("<Key>", self.key_handler)

        self.embed.update()

        self.canvas = PolygonCanvas(C.BLACK, C.WHITE, C.LINE_THICKNESS)

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

    def key_handler(self, event):
        if event.keysym == 'z':
            self.undo()



    def pencil(self):
        self.canvas.color = C.BLACK

    def eraser(self):
        self.canvas.color = C.WHITE

    def red(self):
        self.canvas.color = C.RED

    def green(self):
        self.canvas.color = C.GREEN

    def blue(self):
        self.canvas.color = C.BLUE

    def more(self):
        self.canvas.thickness = C.LINE_THICKNESS + 5

    def less(self):
        self.canvas.thickness = C.LINE_THICKNESS

    def send(self):
        res = self.canvas.resolution()
        new_res = (IMG_WIDTH, round(IMG_WIDTH * res[1] / res[0]))
        img = Image.frombytes("RGBA", res, bytes(self.canvas))
        scaled = img.resize(new_res, Image.Resampling.NEAREST)  # type: ignore
        self.chat.add_image(ImageTk.PhotoImage(scaled), C.USERNAME)

        # try sending to peer
        if network.CONNECTION == True:
            try:
                print("trying to send to peer")
                network.OUTGOING_QUEUE.put(bytes(self.canvas))

            except Exception as e:
                print(f"Failed to send: {e}")

        self.canvas.clear()

    def pygame_loop(self):
        if not self.running:
            return
        self.canvas.do_frame()
        self.chat.receive_drawing()
        self.root.after(10, self.pygame_loop)
