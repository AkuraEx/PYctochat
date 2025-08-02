import tkinter as tk
import os
from app import PictoChatApp
import pyglet

pyglet.options["win32_gdi_font"] = True

os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"
os.environ["SDL_MOUSE_RELATIVE"] = "0"
os.environ["TK_SILENCE_DEPRECATION"] = "1"

os.chdir(os.path.realpath(os.path.dirname(__file__)))

pyglet.font.add_directory("assets/font/pixelifysans/static")

root = tk.Tk()


if __name__ == "__main__":
    app = PictoChatApp(root)
    root.mainloop()
