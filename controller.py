"""Controller for Slide game"""
from model0 import Model
from view import View


class Controller():
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
        self.root = root
        self.size = size
        self.game_over = False
        self.moves = []
        self.model = Model(size)
        self.view = View(root, size)
        self.valid_moves = {
            "Up": lambda: self.model.shift_blocks_up(),
            "Down": lambda: self.model.shift_blocks_down(),
            "Left": lambda: self.model.shift_blocks_left(),
            "Right": lambda: self.model.shift_blocks_right(),
            "s": lambda: self.backdoor()
            }
        self.view.bind_all("<Key>", self.move)
        self.view.new_game_button.config(command=self.new_game)
        coords = self.model.add_new_block()
        val = self.model.value_at(coords[0], coords[1])
        self.view.draw_new(coords, val)
        self.model.subscribe_to_moves(self.update_moves)

    def move(self, user_move):
        """
            Execute one move.
            Expects a user move - as defined by the dictionary valid_moves
            Returns a string when the game is over
        """
        if self.game_over:
            return
        key = user_move.keysym
        if self.view.is_animating():
            return
        no_sliding = self.valid_moves[key]()
        try:
            self.do_moves()
        except IndexError:
            self.view.redraw_from_model()
        game_check = self.model.game_state_check()
        if game_check:
            self.view.game_end(game_check)
            self.game_over = True
        elif not no_sliding:
            coords = self.model.add_new_block()
            val = self.model.value_at(coords[0], coords[1])
            self.view.draw_new(coords, val)
        print(self.model.grid)

    def new_game(self):
        """
           Starts a new game by deleting the model and creating a new one
        """
        self.model = Model(self.size)
        self.game_over = False
        self.view.reset()
        coords = self.model.add_new_block()
        val = self.model.value_at(coords[0], coords[1])
        self.view.draw_new(coords, val)
        self.model.subscribe_to_moves(self.update_moves)

    def update_moves(self, move):
        """
            Collects the moves made by the model
        """
        self.moves.append(move)

    def do_moves(self):
        """
          Executes the moves collected from the model
        """
        fin = self.view.draw_moves(self.moves)
        if fin:
            self.moves = []

    def redraw_from_model(self):
        """
            Has the view redraw the board based on the values in the model.
            Used if
        """
        self.view.reset()
        for x in range(self.size):
            for y in range(self.size):
                val = self.model.value_at(x, y)
                self.view.draw_from_value(x, y, val)

    def backdoor(self):
        for x in range(self.size):
            for y in range(self.size):
                m = (x + y) % 2 == 0
                if m:
                    self.model.add_block_at(x, y, 2)
                    self.view.draw_new((x, y), 2)
                else:
                    self.model.add_block_at(x, y, 4)
                    self.view.draw_new((x, y), 4)
