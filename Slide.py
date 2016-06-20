"""2048 clone playable in python environment."""

from model0 import Model
from view import View
from tkinter import Tk, Frame
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


def newgame():
    """Handle creation of new game.
    Returns a model object"""
    print('Board size?')
    while True:
        try:
            i = int(input())
            print('Board will be ' + str(i) + ' by ' + str(i) + ' in size')
            return Model(i)
        except ValueError:
            print("Give me digits, not letters!")


def exit():
    """exits the game
    Returns none"""
    print('bye')


def gameLoop(cur_controller):
    """Main game loop.
    Returns a string"""
    cur_controller
    while True:
        print("move?")
        user_move = input()
        result = cur_controller.move(user_move)
        if result:
            return result


class controller(Frame):
    """The controller classs.

    Controller for modifying the state of the board with legal moves as per
    the rules of the game.
    """
    valid_moves = None

    def __init__(self, parent, size):
        """Initialize the controller class instance.

        model - the model being used for the game being played
        view - the viewing apparendus used for the game being played
        """
        Frame.__init__(self, parent)
        parent.title('Slide')
        self.model = Model(4)
        self.view = View(self, 4)
        self.valid_moves = {
            "Up": lambda: self.model.shift_blocks_up(),
            "Down": lambda: self.model.shift_blocks_down,
            "Left": lambda: self.model.shift_blocks_left,
            "Right": lambda: self.model.shift_blocks_right
            }
        self.bind_all("<Key>", self.move)

    def move(self, user_move):
        """Execute one move.
        Expects a user move - as defined by the dictionary valid_moves
        Returns None if the game is not over, otherwise a string"""
        key = user_move.keysym
        self.valid_moves[key]()
        print("ok")
        if self.model.game_state_check():
            print(self.model.game_state_check())


if __name__ == '__main__':

    launch()
