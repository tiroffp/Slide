"""View for Slide game"""
# import slideexeceptions
from tkinter import *
from PIL import Image, ImageTk
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

    def draw_block(self, x, y, val):
        """
          Purpose:
            Adds a block to the board at the grid coordinates of x, y of value val
          Arguments:
            x (int): Grid coordinate on the x axis of the block on board
            y (int): Grid coordinate on the y axis of the block on board
            val (int): Value of the block being added
        """
        self._board.draw_block(x, y, val)

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
        color = self.get_block_image(val)
        self.itemconfigure(block, image=color)
        self.itemconfigure(text, text=str(val))

    def get_block_image(self, val):
        """
            Purpose:
                Retrieves the block image for the given value
            Arguments:
                val (int) - value to retrieve color for
            Returns:
                Image for block
        """
        if val:
            # the plus one is because I found this list of colors on the internet
            # and didn't organize them by colors, and the first one is a super jarring
            # bright pink
            color = self.blocklist[int(log(val, BLOCK_BASE_VALUE) + 1)]
        else:
            color = self.blocklist[0]
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
            fin = self.animate(move)
            if fin:
                moves_left.remove(move)
        if moves_left == []:
            self.animating = False
            return "fin"
        else:
            return self.after(ANIMATION_DELAY, self.draw_moves, moves_left)

    def animate(self, move):
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
        old_block = self.find_withtag(old_coord_id)[0]
        old_text = self.find_withtag(old_coord_id + "+")[0]
        if old_x > new_x or old_y > new_y:
            shift = - ANIMATION_SLIDE_MOVEMENT_PER_FRAME
        else:
            shift = ANIMATION_SLIDE_MOVEMENT_PER_FRAME
        if old_x == new_x:
            self.move(old_block, 0, shift)
            self.move(old_text, 0, shift)
            finalize = self.coords(old_block) == list((new_x, new_y))
        else:
            self.move(old_block, shift, 0)
            self.move(old_text, shift, 0)
            finalize = self.coords(old_block) == list((new_x, new_y))
        if finalize:
            self.finalize_move(old_block, new_coord_id, old_text)
            return "fin"

    def finalize_move(self, old_block, new_coord_id, text_id):
        """
            Complete the last steps neccessary in a move animation
        """
        val = self.itemcget(text_id, "text")
        if self.find_withtag(new_coord_id):
            new_val = int(val) * BLOCK_BASE_VALUE
            self.itemconfigure(text_id, text=str(new_val))
            self.delete(new_coord_id)
            self.delete(new_coord_id + "+")
        else:
            new_val = int(val)
        self.itemconfigure(old_block, tag=new_coord_id, image=self.get_block_image(new_val))
        self.itemconfigure(text_id, tag=new_coord_id + "+")

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
            image = Image.new("RGB", (0, 0), COLORS[val])
            block_image = ImageTk.PhotoImage(image)
            self.create_image(x, y, image=block_image, tag=block_id)
            self.create_text(x, y, text=str(val), tag=text_id)
            self.animate_new(block_id, [], 0, val)

    def animate_new(self, block_id, holdref, size, val):
        """
            Purpose:
                animates the addition of a new block to the board
            Arguments:
                block_id (int) - Id of block to animate as new block
                holdref (list) - list of ImageTkPhotoImages. Because Tk doesn't handle
                    images properly this guy needs to hold a reference to them during the animation
                    so they don't get garabage collected
                size (int) - current size of the animated block
        """
        if size < BLOCK_SIZE:
            image = Image.new("RGB", (size, size), COLORS[val])
            block_image = ImageTk.PhotoImage(image)
            holdref.append(block_image)
            self.itemconfigure(block_id, image=block_image)
            self.after(ANIMATION_DELAY, self.animate_new, block_id,
                       holdref, size + ANIMATION_GROWTH, val)
        else:
            self.itemconfigure(block_id, image=self.get_block_image(val))

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
