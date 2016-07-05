"""View for Slide game"""
# import slideexeceptions
from tkinter import *
from math import log
from GlobalConstants import *


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
        parent.iconbitmap('block.ico')
        self.buttons = Buttons(self, span)
        self.buttons.pack()
        self.new_game_button = self.buttons.new_game_button
        self._board = Board(parent, size, span)
        self.pack()

    def draw_new(self, coord, val):
        """
            Purpose:
                adds a new block to the board
            Arguments:
                coord (2tuple) - ints representing x and y position
                val (int) - value of new block
        """
        self._board.draw_new(coord, val)

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

    def draw_moves(self, moves):
        """
            Purpose:
                animates a block move, stopping at its new location on the board
            Arugents:
                moves (list of moves): each move is a tuple: position 0 is the old coords,
                position 2 is the new coords
        """
        return self._board.draw_moves(moves)

    def is_animating(self):
        """
            Purpose:
                Determines if the view is currently animating somthing
            Arugents:
                None
            Returns:
                True if the view is busy animating something, else false
        """
        return self._board.animating

    def game_end(self, game_state):
        """
            Purpose:
                Displays result of game ending (game loss display or game win display)
            Arguments:
                game_state (pos int) - denotes the game state. Expects 1 or 2 (loss or win
                    win respectively), not 0 (game not over)
            Returns:
                None
        """
        self._board.game_end(game_state)

    def draw_from_value(self, x, y, value):
        """
            Purpose:
                Draws a block at the coordinates (x, y) colored based on the value
            Arguments:
                x (int) - x coordinate of the block (in grid number)
                y (int) - y coordinate of the block (in grid number)
                value (int) - value of the block
        """
        self._board.draw_from_value(x, y, self._board.get_block_fill(value))


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
        self.animating = False
        self.block_tags = {}
        self.build_fill_list()
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
        for i in range(size):
            for j in range(size):
                x = self.to_pix(i)
                y = self.to_pix(j)
                self.draw_block(x, y, EMPTY_SQUARE_VALUE)

    def draw_block(self, x, y, val, **kwargs):
        """
            Purpose:
                Draws a block centered on (x, y) with color val on the canvas
            Arguments:
                x (int) - coordinate on the x axis IN PIXELS
                y (int) - coordinate on the y axis IN PIXELS
                val (3 or 6 digit hex value) - color of block to draw
                kwargs:
                    "tag" (string) - tag to give rectangle canvas object.
                                     if not given, sets as ""
                    "size" (int) - side length of block.
                                   if not given, sets as BLOCK_SIZE
            Returns:
                none
        """
        try:
            block_size = kwargs["size"]
        except KeyError:
            block_size = BLOCK_SIZE
        fill = self.get_block_fill(val)
        upper_x = x
        upper_y = y
        # minus one bc tkinter rectangle lower right is defined as just outside the rectangle
        lower_x = x + block_size - 1
        lower_y = y + block_size - 1
        try:
            tag = kwargs["tag"]
        except KeyError:
            tag = ""
        self.create_rectangle(upper_x, upper_y, lower_x, lower_y,
                              fill=fill, width=0, tags=tag)
        if tag:
            text_id = tag + "+"
            prev = self.find_withtag(text_id)
            if prev:
                self.delete(text_id)
            self.create_text(x + (BLOCK_SIZE / 2), y + (BLOCK_SIZE / 2), text=str(val), tag=text_id)

    def build_fill_list(self):
        """
            Purpose:
                Converts the COLORS constant to hex
        """
        self.fill_list = []
        for color in COLORS:
            hex_color = '#%02x%02x%02x' % color
            self.fill_list.append(hex_color)

    def to_pix(self, val):
        """
          Purpose:
            To translate a axis coordinate to its pixel on the actual window
            Coordinates are taken from the top left corner of the grid square
          Arguments:
            Val - a number representing the "grid" coord to be translated
          Returns:
            int - Pixel location of that coord (top right corner) on either axis
        """
        return int(BOARD_BORDER + val * GRID_SQ_SIZE + (BLOCK_BORDER))

    def get_block_fill(self, val):
        """
            Purpose:
                Retrieves the block fill color for the given value
            Arguments:
                val (int) - value to retrieve color for
            Returns:
                fill hex color
        """
        if val > EMPTY_SQUARE_VALUE:
            # the plus one is because I found this list of colors on the internet
            # and didn't organize them by colors, and the first one is a super jarring
            # bright pink
            color = self.fill_list[int(log(val, BLOCK_BASE_VALUE) + 1)]
        else:
            color = self.fill_list[0]
        return color

    def draw_moves(self, moves):
        """
            Purpose:
                animates a block move, stopping at its new location on the board
            Arugents:
                moves (list of moves): each move is a tuple: position 0 is the old coords,
                position 2 is the new coords
        """
        # want a complete copy of the moves list, not just a reference, since it will be editied during
        # the following loop
        self.animating = True
        moves_left = list(moves)
        for move in moves:
            fin = self.animate_move(move)
            if fin:
                moves_left.remove(move)
        if moves_left == []:
            self.animating = False
            return "fin"
        else:
            return self.after(ANIMATION_DELAY, self.draw_moves, moves_left)

    def animate_move(self, move):
        """
            Purpose:
                animates a block move
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
        moving_block = self.find_withtag(old_coord_id)[0]
        try:
            moving_text = self.find_withtag(old_coord_id + "+")[0]
        except IndexError:
            raise Exception("can't find " + str(old_coord_id) + "+")
        if old_x > new_x or old_y > new_y:
            shift = - ANIMATION_SLIDE_ADJ
        else:
            shift = ANIMATION_SLIDE_ADJ
        if old_x == new_x:
            self.move(moving_block, 0, shift)
            self.move(moving_text, 0, shift)
            block_coords = self.coords(moving_block)[0:2]
            diff = abs(new_y - block_coords[1])
            if diff < ANIMATION_SLIDE_ADJ:
                self.move(moving_block, 0, diff)
                self.move(moving_text, 0, diff)
                self.finalize_move(moving_block, new_coord_id, moving_text)
                return "fin"
        else:
            self.move(moving_block, shift, 0)
            self.move(moving_text, shift, 0)
            block_coords = self.coords(moving_block)[0:2]
            diff = abs(new_x - block_coords[0])
            if diff < ANIMATION_SLIDE_ADJ:
                self.move(moving_block, diff, 0)
                self.move(moving_text, diff, 0)
                self.finalize_move(moving_block, new_coord_id, moving_text)
                return "fin"

    def finalize_move(self, moving_block, new_coord_id, moving_text):
        """
            Purpose:
                Cleans up objects & object tags used during animation
            Arguments:
                moving_block (string) - tag of block being moved in animation
                new_coord_id (string) - tag that the block will be assigned at end of move
                moving_text (string) - tag of the text being moved with the block
            Returns:
                None
        """
        val = self.itemcget(moving_text, "text")
        if self.find_withtag(new_coord_id):
            new_val = int(val) * BLOCK_BASE_VALUE
            self.itemconfigure(moving_text, text=str(new_val))
            self.delete(new_coord_id)
            self.delete(new_coord_id + "+")
        else:
            new_val = int(val)
        self.itemconfigure(moving_block, tag=new_coord_id, fill=self.get_block_fill(new_val))
        self.itemconfigure(moving_text, tag=new_coord_id + "+")
        self.tag_raise(moving_text, moving_block)

    def draw_new(self, coord, val):
        """
            Purpose:
                adds a new block to the board
            Arguments:
                coord (2tuple) - ints representing x and y position
                val (int) - value of new block
        """
        if self.animating:
            self.after(ANIMATION_DELAY, self.draw_new, coord, val)
        else:
            x, y = coord
            block_id = str(x) + "," + str(y)
            text_id = block_id + "+"
            x = self.to_pix(x)
            y = self.to_pix(y)
            self.draw_block(x, y, val, tag=block_id, size=0)
            self.animate_new(x, y, block_id, text_id, val, 0)

    def animate_new(self, x, y, block_id, text_id, val, size):
        """
            Purpose:
                animates the addition of a new block to the board
            Arguments:
                x (int) - x coord of block
                y (int) - y coord of block
                block_id (string) - tag of block to animate as new block
                text_id (string) - tag of text to animate with new block
                val (int) - value of block
                size (int) - current size of the animated block
        """
        if size < BLOCK_SIZE:
            self.delete(block_id)
            self.draw_block(x, y, val, tag=block_id, size=size)
            self.after(ANIMATION_DELAY, self.animate_new, x, y, block_id, text_id,
                       val, size + ANIMATION_GROWTH_ADJ)
        else:
            self.delete(block_id)
            self.draw_block(x, y, val, tag=block_id, size=BLOCK_SIZE)
            # self.create_text(x + (BLOCK_SIZE / 2), y + (BLOCK_SIZE / 2), text=str(val), tag=text_id)

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

    def game_end(self, game_state):
        """
            Purpose:
                Displays result of game ending (game loss display or game win display)
            Arguments:
                game_state (pos int) - denotes the game state. Expects 1 or 2 (loss or win
                    win respectively), not 0 (game not over)
            Returns:
                None
            this method was quickly made and therefore gross. sorry
        """
        if game_state == GAME_STATE["Loss"]:
            text = "you lose!"
        else:
            text = "you win!"
        self.create_rectangle(self.span/2 - 50, self.span/2 - 25, self.span/2 + 50, self.span/2 + 25, fill="#FFF")
        self.create_text(self.span/2, self.span/2, text=text)

# Used only when testing view before it was ready to be called by the controller
# def main():

#     root = Tk()
#     nib = View(root)
#     root.mainloop()
#     #Makes SublimeLinter stop warning me "nib is assigned but never used" >:(
#     root = nib

# if __name__ == '__main__':
#     main()
