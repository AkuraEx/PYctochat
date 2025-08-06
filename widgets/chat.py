from tkinter import Frame, Label, Scrollbar, Canvas, Misc, PhotoImage
from PIL import Image, ImageTk
import config as c
import network

type AnyPhotoImage = PhotoImage | ImageTk.PhotoImage

IMG_WIDTH = 234


class Chat(Frame):
    def __init__(self, master: Misc | None, *args, **kwargs):
        super().__init__(master, *args, background="", **kwargs)

        self.messages: list[AnyPhotoImage] = []
        self.labels: list[Label] = []

        self.canvas = Canvas(self, width=c.CHAT_WIDTH, height=c.WINDOW_HEIGHT)
        self.scrollbar = Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # Bind
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Pack them
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.add_image(PhotoImage(file="assets/welcome.png"))

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _reset(self):
        self.canvas.yview_scroll(1, "pages")

    def add_image(self, image: AnyPhotoImage, Username=None):
        assert image.width() == c.CHAT_WIDTH

        if Username:
            name = Label(
                self.scrollable_frame,
                text=Username,
                background=c.USER_COLOR,
                foreground=c.ALT_COLOR,
                highlightbackground=c.ALT_COLOR,
                highlightthickness=1,
                font=("Pixelify Sans", 16),
                padx=20,
                pady=2,
            )

            name.grid(row=len(self.messages), sticky="w")
            self.messages.append(name)
            self.labels.append(name)

        label = Label(self.scrollable_frame, image=image)
        label.grid(row=len(self.messages), sticky="w")

        self.messages.append(image)
        self.labels.append(label)

        self.after_idle(self._reset)

    def receive_drawing(self) -> None:
        try:
            while not network.INCOMING_QUEUE.empty():
                read_bytes = network.INCOMING_QUEUE.get_nowait()
                res = (768, 290)
                new_res = (IMG_WIDTH, round(IMG_WIDTH * res[1] / res[0]))
                img = Image.frombytes("RGBA", res, bytes(read_bytes[1]))
                scaled = img.resize(new_res, Image.Resampling.NEAREST)  # type: ignore
                self.add_image(ImageTk.PhotoImage(scaled), read_bytes[0])

        except Exception as e:
            print(f"Error receiving drawing: {e}")
            pass
