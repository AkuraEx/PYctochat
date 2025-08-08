import tkinter as tk
import os
import trio
from network import run
import argparse
import threading
from app import PictoChatApp
import config as c
import pyglet

pyglet.options["win32_gdi_font"] = True

os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"
os.environ["SDL_MOUSE_RELATIVE"] = "0"

os.chdir(os.path.realpath(os.path.dirname(__file__)))

pyglet.font.add_directory("assets/font/pixelifysans/static")

# Command Line arguments:
# -p specifies port number, -d specifies destination client is connecting to
# -n specifies username, -c specifies color them for user
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", default=0, type=int)
parser.add_argument("-d", "--destination", type=str)
parser.add_argument("-n", "--name", type=str)
parser.add_argument("-c", "--color", type=str)
args = parser.parse_args()

if args.name:
    c.USERNAME = args.name
if args.color == "blue":
    c.USER_COLOR, c.ALT_COLOR = "#0082fb", "#2400f0"
if args.color == "green":
    c.USER_COLOR, c.ALT_COLOR = "#4fda6d", "#16b102"
if args.color == "red":
    c.USER_COLOR, c.ALT_COLOR = "#e45d5d", "#e00404"

# Tkinter init
root = tk.Tk()
root.iconbitmap("assets/pictochatlogo.ico")


def start_trio_network():
    # Trio flavored async function
    trio.run(run, args.port, args.destination)


if __name__ == "__main__":
    # Network thread in the background
    threading.Thread(target=start_trio_network, daemon=True).start()

    # Main app
    app = PictoChatApp(root)
    root.mainloop()
