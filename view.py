"""View for Slide game"""
# import slideexeceptions
from tkinter import Tk, Frame, Canvas, NW
from PIL import Image, ImageTk


COLORS = ((2, 63, 165), (125, 135, 185), (190, 193, 212), (214, 188, 192), (187, 119, 132),
          (142, 6, 59), (74, 111, 227), (133, 149, 225), (181, 187, 227), (230, 175, 185),
          (224, 123, 145), (211, 63, 106), (17, 198, 56), (141, 213, 147), (198, 222, 199),
          (234, 211, 198), (240, 185, 141), (239, 151, 8), (15, 207, 192), (156, 222, 214),
          (213, 234, 231), (243, 225, 235), (246, 196, 225), (247, 156, 212))
BLOCK_SIZE = 50
BOARD_BORDER = 50
GRID_SQ_SIZE = 55
BLOCK_BORDER = GRID_SQ_SIZE - BLOCK_SIZE


class View(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        parent.title('SLIDE')
        self.board = Board(parent, 4)
        self.pack()


class Board(Canvas):
    """
    View for game using tkinter framework
    """

    def __init__(self, parent, size):
        """
        Purpose:
          Creates the window and initial boardview
        Arguments:
          Parent (Tk): something to make Tkinter work
          Size (int): number of blocks in a row/column of the grid
        """
        #The window is sized to fit each 50px block plus a 10px buffer between blocks
        #and a 10px border around them
        span = size * GRID_SQ_SIZE + BOARD_BORDER * 2 + BLOCK_BORDER
        Canvas.__init__(self, width=span, height=span, background="#555",
                        highlightthickness=0)
        self.parent = parent  # parent of this Frame
        self.init_board(size, span)
        self.pack()

    def init_board(self, size, span):
        """
        Purpose:
          Creates the board graphic of all blank grid squares
        Arguments:
          Size (int): number of blocks in a row/column of the board
          Span (int): length/height in pixels of the board
        """
        self.create_rectangle(BOARD_BORDER, BOARD_BORDER,
                              span - BOARD_BORDER, span - BOARD_BORDER,
                              fill="#AAA")
        block = Image.new("RGB", (BLOCK_SIZE, BLOCK_SIZE), "#FFF")
        self.block = ImageTk.PhotoImage(block)
        for i in range(size):
            for j in range(size):
                x = self.to_pix(i)
                y = self.to_pix(j)
                centering_adjustment = int(BLOCK_BORDER)
                self.create_image(x, y,
                                  image=self.block, anchor=NW, tag="0")

    def to_pix(self, val):
        """
        Purpose:
          To translate a axis coordinate to its pixel on the actual window
          Coordinates are taken from the top left corner of the grid square
        Arguments:
          Val - a number representing the "grid" coord to be translated
        Returns:
          Pixel location of that coord on either axis
        """
        return BOARD_BORDER + val * GRID_SQ_SIZE + BLOCK_BORDER


def main():

    root = Tk()
    nib = View(root)
    root.mainloop()
    #Makes SublimeLinter stop warning me "nib is assigned but never used" >:(
    root = nib

if __name__ == '__main__':
    main()