import tkinter as tk
import os
from app import PictoChatApp
import argparse
import threading
import trio
from network import run

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", default=0, type=int)
parser.add_argument("-d", "--destination", type=str)
args = parser.parse_args()

root = tk.Tk()

def start_trio_network():
    trio.run(run, args.port, args.destination)

if __name__ == "__main__":
    threading.Thread(target=start_trio_network, daemon=True).start()
    app = PictoChatApp(root)
    root.mainloop()
