import tkinter as tk
import os
import trio
from network import run
import argparse
import threading
from app import PictoChatApp
import pyglet

pyglet.options["win32_gdi_font"] = True

os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"
os.environ["SDL_MOUSE_RELATIVE"] = "0"

os.chdir(os.path.realpath(os.path.dirname(__file__)))

pyglet.font.add_directory("assets/font/pixelifysans/static")

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", default=0, type=int)
parser.add_argument("-d", "--destination", type=str)
args = parser.parse_args()

root = tk.Tk()
root.iconbitmap("assets/pictochatlogo.ico") 

def start_trio_network():
    trio.run(run, args.port, args.destination)

if __name__ == "__main__":
    threading.Thread(target=start_trio_network, daemon=True).start()
    app = PictoChatApp(root)
    root.mainloop()
