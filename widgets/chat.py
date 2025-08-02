from tkinter import (
    Frame,
    Label,
    Misc,
    PhotoImage,
)
from PIL import ImageTk
import config as C

type AnyPhotoImage = PhotoImage | ImageTk.PhotoImage


class Chat(Frame):
    def __init__(self, master: Misc | None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.messages: list[AnyPhotoImage] = []
        self.labels: list[Label] = []

        self.add_image(PhotoImage(file="assets/welcome.png"))

    def add_image(self, image: AnyPhotoImage):
        assert image.width() == C.CHAT_WIDTH

        label = Label(self, image=image)
        label.grid(row=len(self.messages))

        self.messages.append(image)
