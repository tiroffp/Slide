"""View for Slide game"""
import slideexeceptions
from tkinter import Tk, Frame, Canvas, ALL, NW


COLORS = ((2, 63, 165), (125, 135, 185), (190, 193, 212), (214, 188, 192), (187, 119, 132),
          (142, 6, 59), (74, 111, 227), (133, 149, 225), (181, 187, 227), (230, 175, 185),
          (224, 123, 145), (211, 63, 106), (17, 198, 56), (141, 213, 147), (198, 222, 199),
          (234, 211, 198), (240, 185, 141), (239, 151, 8), (15, 207, 192), (156, 222, 214),
          (213, 234, 231), (243, 225, 235), (246, 196, 225), (247, 156, 212))


class View(Frame):
    """
    View for game using tkinter framework
    """

    def __init__(self, parent, size):
        Canvas.__init__(self, width=size + 20, height=size+20,
                        background="black", highlightthickness=0)
        self.parent = parent
        self.initGame(size)
        self.pack()

    def initGame(self, size):
        pass


def main():

    root = Tk()
    nib = View(root)
    root.mainloop()


if __name__ == '__main__':
    main()
