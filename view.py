"""View for Slide game"""
# import slideexeceptions
from tkinter import *
from PIL import Image, ImageTk
from math import log


COLORS = ((265, 265, 265), (265, 63, 165), (125, 135, 185), (190, 193, 212), (214, 188, 192), (187, 119, 132),
          (142, 6, 59), (74, 111, 227), (133, 149, 225), (181, 187, 227), (230, 175, 185),
          (224, 123, 145), (211, 63, 106), (17, 198, 56), (141, 213, 147), (198, 222, 199),
          (234, 211, 198), (240, 185, 141), (239, 151, 8), (15, 207, 192), (156, 222, 214),
          (213, 234, 231), (243, 225, 235), (246, 196, 225), (247, 156, 212))
BLOCK_SIZE = 50
BOARD_BORDER = 50
GRID_SQ_SIZE = 55
BLOCK_BORDER = GRID_SQ_SIZE - BLOCK_SIZE


class View(Frame):

    def __init__(self, parent, size):
        """
            Purpose:
                Creates window for program
            Arguments:
                Parent (Tk): Tk object running the view
                size (int): size of board
        """
        Frame.__init__(self, parent)
        span = size * GRID_SQ_SIZE + BOARD_BORDER * 2 + BLOCK_BORDER
        parent.minsize(span, span)
        parent.title('Slide')
        self.buttons = Buttons(self, span)
        self.buttons.pack()
        self.new_game_button = self.buttons.new_game_button
        self._board = Board(parent, size, span)
        self.pack()

    def draw_block(self, x, y, val):
        self._board.draw_block(x, y, val)

    def draw_move(self, move):
        self._board.draw_move(move)

    def draw_new(self, coord):
        self._board.draw_new(coord)

    def reset(self):
        """
            Purpose:
                Resets the board back to just-after-init state
            Arguments:
                None
            Returns:
                None
        """
        self._board.wipe_board()


class Buttons(Frame):

    def __init__(self, parent, span):
        Frame.__init__(self, parent, width=span, height=24)
        self.new_game_button = Button(self, text='New Game', background="#AAA")
        self.new_game_button.pack(fill=X)

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)


class Board(Canvas):
    """
        View for game using tkinter framework
    """

    def __init__(self, parent, size, span):
        """
          Purpose:
            Creates the window and initial boardview
          Arguments:
            Parent (Tk): something to make Tkinter work
            Size (int): number of blocks in a row/column of the grid
        """
        #The window is sized to fit each 50px block plus a 10px buffer between blocks
        #and a 10px border around them
        Canvas.__init__(self, width=span, height=span, background="#555",
                        highlightthickness=0)
        self.parent = parent  # parent of this Frame
        self.size = size
        self.span = span
        self.valblock = ImageTk.PhotoImage(Image.new("RGB", (BLOCK_SIZE, BLOCK_SIZE), (2, 63, 165)))
        self.block_tags = {}
        self.build_blocklist()
        self.build_board(size, span)
        self.pack()

    def build_board(self, size, span):
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
        grid_sq = Image.new("RGB", (BLOCK_SIZE, BLOCK_SIZE), "#FFF")
        self.grid_sq = ImageTk.PhotoImage(grid_sq)
        for x in range(size):
            for y in range(size):
                ex = self.to_pix(x)
                why = self.to_pix(y)
                self.create_image(ex, why, image=self.grid_sq)

    def build_blocklist(self):
        """
            Takes the Colors global and builds a list of ImageTk objects to  use
            when drawing blocks
        """
        self.blocklist = []
        for color in COLORS:
            image = Image.new("RGB", (BLOCK_SIZE, BLOCK_SIZE), color)
            block_image = ImageTk.PhotoImage(image)
            self.blocklist.append(block_image)

    def to_pix(self, val):
        """
          Purpose:
            To translate a axis coordinate to its pixel on the actual window
            Coordinates are taken from the top left corner of the grid square
          Arguments:
            Val - a number representing the "grid" coord to be translated
          Returns:
            int - Pixel location of that coord on either axis
        """
        return int(BOARD_BORDER + val * GRID_SQ_SIZE + (BLOCK_BORDER + GRID_SQ_SIZE) / 2)

    def draw_block(self, x, y, val):
        """
          Purpose:
            Adds a block to the board at the grid coordinates of x, y of value val
          Arguments:
            x (int): Grid coordinate on the x axis of the block on board
            y (int): Grid coordinate on the y axis of the block on board
            val (int): Value of the block being added
        """
        coord = str(x) + "," + str(y)
        coord_text = coord + "+"
        block = self.find_withtag(coord)[0]
        text = self.find_withtag(coord_text)[0]
        x = self.to_pix(x)
        y = self.to_pix(y)
        color = self.get_color(val)
        self.itemconfigure(block, image=color)
        self.itemconfigure(text, text=str(val))

    def get_color(self, val):
        """
            Purpose:
                Retrieves the color block for the given value
            Arguments:
                val (int) - value to retrieve color for
            Returns:
                Image for block
        """
        if val:
            # the plus one is because I found this list of colors on the internet
            # and didn't organize them by colors, and the first one is a super jarring
            # bright pink
            color = self.blocklist[int(log(val, 2) + 1)]
        else:
            color = self.blocklist[0]
        return color

    def draw_move(self, move):
        """
            Purpose:
                animates a block move, stopping at its new location on the board
            Arugents:
                move (tuple of two coords): position 0 is the old coords, position 2
                is the new coords
        """
        old_coord, new_coord = move
        old_x, old_y = old_coord
        new_x, new_y = new_coord
        old_x = self.to_pix(old_x)
        old_y = self.to_pix(old_y)
        new_x = self.to_pix(new_x)
        new_y = self.to_pix(new_y)
        old_coord_id = str(old_coord[0]) + "," + str(old_coord[1])
        new_coord_id = str(new_coord[0]) + "," + str(new_coord[1])
        old_block = self.find_withtag(old_coord_id)[0]
        # if old_x > new_x or old_y > new_y:
        #     shift = -1
        # else:
        #     shift = 1
        # if old_x == new_x:
        #     cur_y = old_y
        #     while cur_y != new_y:
        #         self.move(old_block, old_x, shift)
        #         cur_y += shift
        # else:
        #     cur_x = old_x
        #     while cur_x != new_x:
        #         self.move(old_block, shift, old_y)
        #         cur_x += shift
        self.move(old_block, new_x - old_x, new_y - old_y)
        old_text = self.find_withtag(old_coord_id + "+")[0]
        self.move(old_text, new_x - old_x, new_y - old_y)
        val = self.itemcget(old_text, "text")
        if self.find_withtag(new_coord_id):
            new_val = int(val) * 2
            self.itemconfigure(old_text, text=str(new_val))
            self.delete(new_coord_id)
            self.delete(new_coord_id + "+")
        else:
            new_val = int(val)
        self.itemconfigure(old_block, tag=new_coord_id, image=self.get_color(new_val))
        self.itemconfigure(old_text, tag=new_coord_id + "+")

    def draw_new(self, coord):
        """
            Purpose:
                adds a new block to the board
            Arguments:
                coord (2tuple) - ints representing x and y position
        """
        x, y = coord
        block_id = str(x) + "," + str(y)
        text_id = block_id + "+"
        block = self.get_color(2)
        x = self.to_pix(x)
        y = self.to_pix(y)
        self.create_image(x, y, image=block, tag=block_id)
        self.create_text(x, y, text=str(2), tag=text_id)

    def wipe_board(self):
        """
            Purpose:
                Removes all items from the canvas, then redraws the board to
                just-after-init state
            Arguments:
                None
            Returns:
                None
        """
        for id in self.find_all():
            self.delete(id)
        self.build_board(self.size, self.span)

# Used only when testing view before it was ready to be called by the controller
# def main():

#     root = Tk()
#     nib = View(root)
#     root.mainloop()
#     #Makes SublimeLinter stop warning me "nib is assigned but never used" >:(
#     root = nib

# if __name__ == '__main__':
#     main()
