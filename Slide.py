"""2048 clone playable in python environment."""

from model0 import Model as model
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
        print('Welcome to:')
        print(title)
        print('start new game? (Y/N)')
        i = input()
        if i == 'Y' or i == 'y':
            game_model = newgame()
        else:
            exit()
            return "the game has exited"
        game_controller = controller(model=game_model, view=None)
        print(gameLoop(game_controller))


def newgame():
    """Handle creation of new game.
    Returns a model object"""
    print('Board size?')
    while True:
        try:
            i = int(input())
            print('Board will be ' + str(i) + ' by ' + str(i) + ' in size')
            return model(i)
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


class controller:
    """The controller classs.

    Controller for modifying the state of the board with legal moves as per
    the rules of the game.
    """
    valid_moves = None

    def __init__(self, model, view):
        """Initialize the controller class instance.

        model - the model being used for the game being played
        view - the viewing apparendus used for the game being played
        """
        self.model = model
        self.view = view
        self.valid_moves = {
            "up": lambda: self.model.shift_blocks_up(),
            "down": lambda: self.model.shift_blocks_down,
            "left": lambda: self.model.shift_blocks_left,
            "right": lambda: self.model.shift_blocks_right
            }

    def move(self, user_move):
        """Execute one move.
        Expects a user move - as defined by the dictionary valid_moves
        Returns None if the game is not over, otherwise a string"""
        try:
            self.valid_moves[user_move]()
            print("ok")
        except KeyError:
            print('valid moves:')
            for key in self.valid_moves:
                print(key)
        self.model.add_new_block()
        if self.model.game_state_check():
            return self.model.game_state_check()
            print(self.model.game_state_check())


if __name__ == '__main__':

    launch()
