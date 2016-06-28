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
        self.moves = []
        self.model = Model(size)
        self.view = View(root, size)
        self.valid_moves = {
            "Up": lambda: self.model.shift_blocks_up(),
            "Down": lambda: self.model.shift_blocks_down(),
            "Left": lambda: self.model.shift_blocks_left(),
            "Right": lambda: self.model.shift_blocks_right()
            }
        self.view.bind_all("<Key>", self.move)
        self.view.new_game_button.config(command=self.new_game)
        # self.render_board()
        self.view.draw_new(self.model.add_new_block())
        self.model.subscribe_to_moves(self.update_moves)

    def move(self, user_move):
        """
            Execute one move.
            Expects a user move - as defined by the dictionary valid_moves
            Returns a string when the game is over
        """
        key = user_move.keysym
        no_sliding = self.valid_moves[key]()
        self.do_moves()
        if self.model.game_state_check():
            print(self.model.game_state_check())
        elif not no_sliding:
            self.view.draw_new(self.model.add_new_block())

    def render_board(self):
        """
            Instructs the view to draw the whole gameboard
        """
        for x in range(self.size):
            for y in range(self.size):
                val = self.model.value_at(x, y)
                self.view.draw_block(x, y, val)

    def new_game(self):
        """
           Starts a new game by deleting the model and creating a new one
        """
        self.model = Model(self.size)
        self.view.reset()
        self.view.draw_new(self.model.add_new_block())
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
