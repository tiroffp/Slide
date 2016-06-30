"""2048 clone playable in python environment."""
from tkinter import Tk
from controller import Controller
from GlobalConstants import *


def launch():
    """Main function of module.
    Returns a string"""
    root = Tk()
    Controller(root, SIZE)
    root.mainloop()

if __name__ == '__main__':

    launch()
