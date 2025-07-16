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

        self.button_frame = Frame(self.root, bg="white")
        self.button_frame.place(x=0, y=0, width=100, height=C.WINDOW_HEIGHT)

        self.clrIcon = PhotoImage(file="assets/pictochatlogo.png")
        self.quitIcon = PhotoImage(file="assets/close.png")
        self.pencilIcon = PhotoImage(file="assets/pencil.png")
        self.eraserIcon = PhotoImage(file="assets/eraser.png")
        self.moreIcon = PhotoImage(file="assets/more.png")
        self.lessIcon = PhotoImage(file="assets/less.png")

        clrButton = Button(
            self.button_frame,
            text="Clear",
            command=self.clear,
            image=self.clrIcon,
        )
        clrButton.place(x=5, y=480)

        quitButton = Button(
            self.button_frame,
            text="Quit",
            command=self.quit,
            image=self.quitIcon,
        )
        quitButton.place(x=5, y=0)
        pencilButton = Button(
            self.button_frame,
            text="Pencil",
            command=self.pencil,
            image=self.pencilIcon,
        )
        pencilButton.place(x=5, y=300)
        eraserButton = Button(
            self.button_frame,
            text="Eraser",
            command=self.eraser,
            image=self.eraserIcon,
        )
        eraserButton.place(x=5, y=340)
        moreButton = Button(
            self.button_frame,
            text="More",
            command=self.more,
            image=self.moreIcon,
        )
        moreButton.place(x=5, y=400)
        lessButton = Button(
            self.button_frame,
            text="Less",
            command=self.less,
            image=self.lessIcon,
        )
        lessButton.place(x=5, y=440)

        self.canvas = PolygonCanvas(
            C.CANVAS, C.BLACK, C.WHITE, C.LINE_THICKNESS
        )

        self.root.after(10, self.pygame_loop)

    def clear(self):
        self.canvas.clear()

    def quit(self):
        self.running = False
        pygame.quit()
        self.root.destroy()

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
