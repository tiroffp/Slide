"""View for Slide game"""
# import slideexeceptions
from tkinter import Tk, Frame, Canvas, ALL, NW
from PIL import Image, ImageTk


COLORS = ((2, 63, 165), (125, 135, 185), (190, 193, 212), (214, 188, 192), (187, 119, 132),
          (142, 6, 59), (74, 111, 227), (133, 149, 225), (181, 187, 227), (230, 175, 185),
          (224, 123, 145), (211, 63, 106), (17, 198, 56), (141, 213, 147), (198, 222, 199),
          (234, 211, 198), (240, 185, 141), (239, 151, 8), (15, 207, 192), (156, 222, 214),
          (213, 234, 231), (243, 225, 235), (246, 196, 225), (247, 156, 212))
BLOCK_SIZE = 50
BORDER_SIZE = 10


class View(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        parent.title('SLIDE')
        self.board = Board(parent)
        self.pack()


class Board(Canvas):
    """
    View for game using tkinter framework
    """

    def __init__(self, parent, size=4):
        """
        Creates the window and initial boardview
        Expects the number of blocks in the game as the size argument
        """
        #The window is sized to fit each 50px block plus a 10px buffer between blocks
        #and a 10px border around them
        span = (size * BLOCK_SIZE) + (size * BORDER_SIZE) + BORDER_SIZE
        Canvas.__init__(self, width=span, height=span, background="#555",
                        highlightthickness=0)
        self.parent = parent  # parent of this Frame
        self.blocks = []
        self.create_rectangle(10, 10, span - 10, span - 10, fill="#AAA")
        for i in range(size):
            for j in range(size):
                block = Image.new("RGB", (BLOCK_SIZE, BLOCK_SIZE), COLORS[0])
                blocktk = ImageTk.PhotoImage(block)
                x = self.to_pix(i)
                y = self.to_pix(j)
                self.create_image(x, y, image=blocktk, anchor=NW,  tag="0")
        self.pack()

    def init_game(self, size):
        block = Image.new("RGB", (BLOCK_SIZE, BLOCK_SIZE), COLORS[0])
        self.blocks.append(ImageTk.PhotoImage(block))
        # self.create_block(

    def to_pix(self, val):
        return val + 10 * 50


def main():

    root = Tk()
    nib = View(root)
    root.mainloop()


if __name__ == '__main__':
    main()
