"""Model for Slide game - keeps data in a double array, such that Model[x][y]
refers to the value at (x,y) on the grid displayed to the user."""
import random
import slideexceptions


class Model:

    size = None
    game_states = {"Win": "you win!", "Loss": "you lose!", "Play": 0}
    _unoccupied_squares = None
    game_goal = 2048
    _empty_square_value = 0
    _new_block_value = 2

    def __init__(self, num):
        """
        Initilizes the model to represent a start board -
        A board of the given size with only one randomly placed block of value 2
        Will throw TypeError if num is not an integer greater than or equal to 2
        """
        if num < 2:
            raise TypeError('Arugment number must be larger than 2')
        self.size = int(num)
        self._unoccupied_squares = []
        l = []
        for i in range(num):
            m = []
            for j in range(num):
                coordinate = i, j
                self._unoccupied_squares.append(coordinate)
                m.append(self._empty_square_value)
            l.append(m)
        self._grid = l
        self.add_new_block()

    def add_block_at(self, x, y, value):
        """
        Adds a block at a specific point on the board
        Overwrites any value that is at the coordinate defined by (x,y)
        Does not check to see if coordinate is valid before adding
        """
        self._grid[x][y] = value
        if (x, y) in self._unoccupied_squares and value != self._empty_square_value:
            self._unoccupied_squares.remove((x, y))
        elif value == self._empty_square_value:
            self._unoccupied_squares.append((x, y))
        # print(value)
        # print((x,y))
        # print(self._unoccupied_squares)

    def add_new_block(self):
        """
        Adds a new block to a random non-occupied (value of zero) square on the board
        """
        if len(self._unoccupied_squares) == 0:
            raise slideexceptions.AddBlockError("GameBoard is Full")
        new_x, new_y = self._unoccupied_squares.pop(int(random.random() * len(self._unoccupied_squares)))
        self._grid[new_x][new_y] = self._new_block_value

    def value_at(self, x, y):
        """Gets the value of the grid at the coordinate (x,y) on the board."""
        return self._grid[x][y]

    def count_blocks(self):
        """
        Counts the number of blocks on the board
        Returns an integer representing the number of blocks on the board
        """
        result = 0
        for i in range(self.size):
            for j in range(self.size):
                b = self.value_at(i, j)
                if b > self._empty_square_value:
                    result += 1
        return result

    def shift_blocks_left(self):
        """
        Shifts all blocks left and collapses same-valued blocks into their left neighbor
        """
        self._shift_blocks(1, 1)

    def shift_blocks_right(self):
        """
        Shifts all blocks right and collapses same-valued blocks
        """
        self._shift_blocks(1, 0)

    def shift_blocks_up(self):
        """
        Shifts all blocks up and collapses same-valued blocks
        """
        self._shift_blocks(0, 0)

    def shift_blocks_down(self):
        """
        Shifts all blocks down and collapses same-valued blocks
        """
        self._shift_blocks(0, 1)

    def _shift_blocks(self, shift_horizontal, shift_to_bottom_left):
        """
        Abstraction for shifting blocks in a direction
        Takes two arguements:
        shift_horizontal: Boolean - True means movement left-right, False means up-down
        shift_to_bottom_left: Boolean - True means movement toward origin(down,left), false means away(up,right)
        this means that the four direction have the following arguments:
        Left:  self._shift_blocks(1,1)
        Right: self._shift_blocks(1,0)
        Up:    self._shift_blocks(0,0)
        Down:  self._shift_blocks(0,1)
        """
        for outer_iteration_value in range(self.size):
            last_block_val = self._empty_square_value
            if shift_to_bottom_left:
                last_open = 0
            else:
                last_open = self.size - 1
            for inner_iteration_value in range(self.size):
                if shift_to_bottom_left:
                    directional_adjustment = -1
                else:
                    inner_iteration_value = self.size - inner_iteration_value - 1
                    directional_adjustment = 1
                if shift_horizontal:
                    x_coord_old = inner_iteration_value
                    y_coord_old = outer_iteration_value
                else:
                    x_coord_old = outer_iteration_value
                    y_coord_old = inner_iteration_value
                val = self._grid[x_coord_old][y_coord_old]
                if val > self._empty_square_value and val == last_block_val:
                    last_block_val = val + val
                    self._block_merge(last_block_val, x_coord_old, y_coord_old, last_open,
                                      directional_adjustment, shift_horizontal, shift_to_bottom_left)
                elif val > self._empty_square_value:
                    self._block_collide(val, x_coord_old, y_coord_old, last_open,
                                        shift_horizontal, shift_to_bottom_left)
                    last_block_val = val
                    last_open = last_open + (0 - directional_adjustment)

    def _block_merge(self, new_val, x_coord_old, y_coord_old, last_open, directional_adjustment,
                     shift_horizontal, shift_to_bottom_left):
        """
        Handles blocks of same value colliding with eachother and becoming a single block of twice
        their value
        """
        if shift_horizontal:
            x_coord_new = last_open + directional_adjustment
            y_coord_new = y_coord_old
        else:
            x_coord_new = x_coord_old
            y_coord_new = last_open + directional_adjustment
        self._grid[x_coord_new][y_coord_new] = new_val
        self._grid[x_coord_old][y_coord_old] = self._empty_square_value
        self._unoccupied_squares.append((x_coord_old, y_coord_old))

    def _block_collide(self, new_val, x_coord_old, y_coord_old, last_open, shift_horizontal,
                       shift_to_bottom_left):
        """
        Handles blocks moving and colliding with their right-most obstacle
        (wall or block of different value)
        """
        if shift_horizontal:
            x_coord_new_slide = last_open
            y_coord_new_slide = y_coord_old
        else:
            x_coord_new_slide = x_coord_old
            y_coord_new_slide = last_open
        self._grid[x_coord_old][y_coord_old] = 0
        self._grid[x_coord_new_slide][y_coord_new_slide] = new_val

    def game_state_check(self):
        """
        Returns the state of the game, which is one of the three values in the game_states
        class dictionary
        """
        column_maxes = []
        for column in self._grid:
            column_maxes.append(max(column))
        board_max = max(column_maxes)
        if board_max == self.game_goal:
            return self.game_states["Win"]
        if len(self._unoccupied_squares) == 0:
            return self.game_states["Loss"]
        return self.game_states["Play"]
