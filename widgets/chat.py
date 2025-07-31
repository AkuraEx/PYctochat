from tkinter import Frame, Label, Misc, PhotoImage


class Chat(Frame):
    def __init__(self, master: Misc | None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.label = Label(self, text="Chat")
        self.label.pack(side="top")

        self.messages: list[PhotoImage] = []

    def add_image(self, data: bytes):
        image = PhotoImage(master=self, data=data)
        self.messages.append(image)
