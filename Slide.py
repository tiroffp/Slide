"""2048 clone playable in python environment."""

from model0 import Model
from view import View
from tkinter import Tk
title = """
.----------------.  .----------------.  .----------------.  .----------------.  .----------------.
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |    _______   | || |   _____      | || |     _____    | || |  ________    | || |  _________   | |
| |   /  ___  |  | || |  |_   _|     | || |    |_   _|   | || | |_   ___ `.  | || | |_   ___  |  | |
| |  |  (__ \_|  | || |    | |       | || |      | |     | || |   | |   `. \ | || |   | |_  \_|  | |
| |   '.___`-.   | || |    | |   _   | || |      | |     | || |   | |    | | | || |   |  _|  _   | |
| |  |`\____) |  | || |   _| |__/ |  | || |     _| |_    | || |  _| |___.' / | || |  _| |___/ |  | |
| |  |_______.'  | || |  |________|  | || |    |_____|   | || | |________.'  | || | |_________|  | |
| |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'
 """


def launch():
    """Main function of module.
    Returns a string"""
    root = Tk()
    controller(root, 4)
    root.mainloop()


class controller():
    """
        The controller classs.

        Controller for modifying the state of the board with legal moves as per
        the rules of the game.
    """

    def __init__(self, root, size):
        """
            Initialize the controller class instance.

            root - Tk object to handle view
            size - size of board
        """
        self.size = size
        self.model = Model(size)
        self.view = View(root, size)
        self.valid_moves = {
            "Up": lambda: self.model.shift_blocks_up(),
            "Down": lambda: self.model.shift_blocks_down(),
            "Left": lambda: self.model.shift_blocks_left(),
            "Right": lambda: self.model.shift_blocks_right()
            }
        self.view.bind_all("<Key>", self.move)
        self.render_board()

    def move(self, user_move):
        """
            Execute one move.
            Expects a user move - as defined by the dictionary valid_moves
            Returns a string when the game is over
        """
        key = user_move.keysym
        self.valid_moves[key]()
        x, y = self.model.add_new_block()
        self.render_board()
        if self.model.game_state_check():
            print(self.model.game_state_check())

    def render_board(self):
        """
        Instructs the view to draw the whole gameboard
        """
        for x in range(self.size):
            for y in range(self.size):
                val = self.model.value_at(x, y)
                self.view.draw_block(x, y, val)


if __name__ == '__main__':

    launch()
